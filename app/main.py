from typing import Union

from fastapi import FastAPI

# load dotenv
from dotenv import load_dotenv
from claim_extractor import ClaimExtractor

load_dotenv()

app = FastAPI()


@app.post("/process/{file_name}")
def process_paper(file_name: str):
    # load the paper
    file_path = f"./data/{file_name}"
    
    claims = ClaimExtractor().extract_claims(file_path)
    
    print(claims)
    
    # open ai call to break down claims & citations
    return {"Hello": "World"}
