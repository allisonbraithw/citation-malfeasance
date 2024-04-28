"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import os
import hashlib
import google.generativeai as genai
from dotenv import load_dotenv
import ast
from pypdf import PdfReader

from models import ClaimWithReferences

load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

BASE_PROMPT = f'''
Identify the cited claims made in this paper and return a list of the claims, and the references provided to support them.

For example, 
  [
    ("In order to leverage pre-trained unimodal models for VLP, it is key to facilitate cross-modal alignment. However, since
    LLMs have not seen images during their unimodal pretraining, freezing them makes vision-language alignment
    in particular challenging. In this regard, existing methods(<ref1>, <ref2> ) resort to an image-to-text generation loss,
    which we show is insufficient to bridge the modality gap" , [Tsimpoukelli et al., 2021, Alayrac et al., 2022])
  ]
  
Please only return a list of this json format {ClaimWithReferences(claim="example claim", references=["ref1", "ref2"]).model_dump_json()}
'''

# Python class for the claim extractor
class ClaimExtractor:
  def __init__(self, model_name="gemini-1.5-pro-latest"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    self.model = genai.GenerativeModel(model_name=model_name)
    self.uploaded_files = []

  def extract_pdf_pages(self, pathname: str) -> list[str]:
    parts = [f"--- START OF PDF ${pathname} ---"]
    pdf_reader = PdfReader(pathname)


    for index, page in enumerate(pdf_reader.pages):
      parts.append(f"--- PAGE {index} ---")
      parts.append(page.extract_text())
    print(parts)
    return parts

  def extract_claims(self, pdf_path: str) -> str:
    convo = self.model.start_chat(history=[
      {
        "role": "user",
        "parts": self.extract_pdf_pages(pdf_path)
      },
      {
        "role": "user",
        "parts": [BASE_PROMPT]
      },
    ])
    convo.send_message(BASE_PROMPT)
    print(convo.last.text)
    # response = sample_response
    # print(response)
    # parse sample response into a list of ClaimWithReferences:
    # claims = []
    # for claim, references in ast.literal_eval(response):
    #   claims.append(ClaimWithReferences(claim=claim, references=references))
    # print(claims)
    return 'hi'
    # return convo.last.text
  
  def cleanup(self):
    for uploaded_file in self.uploaded_files:
      genai.delete_file(name=uploaded_file.name)
