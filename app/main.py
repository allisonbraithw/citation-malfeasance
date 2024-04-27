from typing import Union

from fastapi import FastAPI

# load dotenv
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.post("/process/{item_id}")
def process_paper():
    # load the paper
    
    # open ai call to break down claims & citations
    return {"Hello": "World"}
