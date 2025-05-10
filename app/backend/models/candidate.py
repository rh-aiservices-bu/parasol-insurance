from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db_utils import Base

class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    primary_skills = Column(String(200), nullable=False)
    tech_stack = Column(String(200))
    experience_years = Column(Float)
    hourly_rate_min = Column(Float)
    hourly_rate_max = Column(Float)
    availability_date = Column(Date)
    location = Column(String(100))
    remote_preference = Column(String(20))  # On-site, Remote, Hybrid
    certifications = Column(String(200))
    education = Column(String(200))
    previous_clients = Column(String(300))
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    opportunity_matches = relationship('CandidateMatch', backref='candidate')

    def to_dict(self, include_match_details=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'primary_skills': self.primary_skills,
            'tech_stack': self.tech_stack,
            'experience_years': self.experience_years,
            'hourly_rate_min': self.hourly_rate_min,
            'hourly_rate_max': self.hourly_rate_max,
            'availability_date': self.availability_date.isoformat() if self.availability_date else None,
            'location': self.location,
            'remote_preference': self.remote_preference,
            'certifications': self.certifications,
            'education': self.education,
            'previous_clients': self.previous_clients,
            'last_updated': self.last_updated.isoformat()
        }
        
        if include_match_details and self.opportunity_matches:
            data['opportunity_matches'] = [match.to_dict() for match in self.opportunity_matches]
            
        return data 