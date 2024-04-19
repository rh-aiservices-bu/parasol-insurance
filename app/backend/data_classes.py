from pydantic import BaseModel
from typing import List, Optional

# Data classes
class ClaimImage(BaseModel):
    """Image related to a claim"""
    image_name: str = ""
    image_key: str = ""

class ClaimBaseInfo(BaseModel):
    """Basic information about a claim"""
    id: int = ""
    claim_number: Optional[str] = ""
    category: Optional[str] = ""
    policy_number: Optional[str] = ""
    client_name: Optional[str] = ""
    subject: str = ""
    summary: Optional[str] = ""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "id": 1,
                "subject": "Claim for Recent Car Accident - Policy Number: ABC12345",
                "summary": "I was driving on the highway when a car hit me from behind. I was not injured but my car was damaged.",
                }
            ]
        }
    }

class ClaimCreationInfo(BaseModel):
    """Basic information needed to create a claim"""
    id: int = ""
    subject: str = ""
    body: str = ""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "id": 1,
                "subject": "Claim for Recent Car Accident - Policy Number: ABC12345",
                "summary": "I was driving on the highway when a car hit me from behind. I was not injured but my car was damaged.",
                }
            ]
        }
    }

class ClaimFullInfo(BaseModel):
    """All information about a claim"""
    id: int = ""
    claim_number: str = ""
    category: str = ""
    policy_number: str = ""
    client_name: str = ""
    subject: str = ""
    body: str = ""
    summary: Optional[str] = ""
    sentiment: Optional[str] = ""
    location: Optional[str]= ""
    time: Optional[str] = ""
    original_images: Optional[List[ClaimImage]] = []
    processed_images: Optional[List[ClaimImage]] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "id": 1,
                "subject": "Claim for Recent Car Accident - Policy Number: ABC12345",
                "body": "<p>Dear XYZ Insurance Company,</p>...",
                "sentiment": "positive",
                "location": "New York, NY",
                "time": "2020-10-10 10:10:10",
                "original_images": [
                    {
                    "image_name": "car1.png",
                    "image_key": "original-images/car1.png"
                    }
                ],
                "processed_images": [
                    {
                    "image_name": "car1.png",
                    "image_key": "processed-images/new_car1.png"
                    }
                ]
            }
            ]
        }
    }