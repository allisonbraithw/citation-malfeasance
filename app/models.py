# pydantic models for relevant objects
from pydantic import BaseModel
from typing import List, Tuple

# model for Claim with references: List[Tuple[claim , List<reference>]]
class ClaimWithReferences(BaseModel):
    claim: str
    references: List[str]
