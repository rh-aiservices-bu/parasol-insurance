from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

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

class OpportunityBase(BaseModel):
    client_company: str
    opportunity_type: str
    tech_stack: Optional[str] = None
    project_duration: Optional[int] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    start_date: Optional[datetime] = None
    location: Optional[str] = None
    remote_status: Optional[str] = None
    resources_count: Optional[int] = None
    seniority_levels: Optional[str] = None
    required_certs: Optional[str] = None
    competition_status: Optional[str] = None
    opportunity_source: Optional[str] = None
    sales_stage: str = "Initial Contact"
    probability: float = 0.0
    sales_rep_id: Optional[int] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    pass

class OpportunityInDB(OpportunityBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True

class CandidateBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    primary_skills: str
    tech_stack: Optional[str] = None
    experience_years: Optional[float] = None
    hourly_rate_min: Optional[float] = None
    hourly_rate_max: Optional[float] = None
    availability_date: Optional[datetime] = None
    location: Optional[str] = None
    remote_preference: Optional[str] = None
    certifications: Optional[str] = None
    education: Optional[str] = None
    previous_clients: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(CandidateBase):
    pass

class CandidateInDB(CandidateBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

class SalesRepresentativeBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    territory: Optional[str] = None
    tech_domain: Optional[str] = None
    quota: Optional[float] = None
    ytd_sales: float = 0.0
    win_rate: float = 0.0

class SalesRepresentativeCreate(SalesRepresentativeBase):
    pass

class SalesRepresentativeUpdate(SalesRepresentativeBase):
    pass

class SalesRepresentativeInDB(SalesRepresentativeBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True

class CandidateMatchBase(BaseModel):
    opportunity_id: int
    candidate_id: int
    match_score: float
    skill_match_pct: float
    rate_match_pct: float
    availability_match: bool
    notes: Optional[str] = None

class CandidateMatchCreate(CandidateMatchBase):
    pass

class CandidateMatchUpdate(CandidateMatchBase):
    pass

class CandidateMatchInDB(CandidateMatchBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True

class OpportunityAnalysis(BaseModel):
    opportunity: OpportunityInDB
    qualification_score: float
    extracted_skills: List[str]
    candidate_matches: List[CandidateMatchInDB]
    pricing_recommendation: dict

class SalesRepPerformance(BaseModel):
    sales_rep: SalesRepresentativeInDB
    performance: dict