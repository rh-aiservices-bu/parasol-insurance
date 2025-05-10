from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.backend.db_utils import Base

class Opportunity(Base):
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True)
    client_company = Column(String(100), nullable=False)
    opportunity_type = Column(String(50), nullable=False)
    tech_stack = Column(String(200))
    project_duration = Column(Integer)  # in months
    budget_min = Column(Float)
    budget_max = Column(Float)
    start_date = Column(Date)
    location = Column(String(100))
    remote_status = Column(String(20))  # On-site, Remote, Hybrid
    resources_count = Column(Integer)
    seniority_levels = Column(String(100))
    required_certs = Column(String(200))
    competition_status = Column(String(100))
    opportunity_source = Column(String(50))
    sales_stage = Column(String(30))
    probability = Column(Float)
    created_date = Column(DateTime, default=datetime.utcnow)
    sales_rep_id = Column(Integer, ForeignKey('sales_representatives.id'))
    
    # Relationships
    sales_rep = relationship('SalesRepresentative', backref='opportunities')
    candidate_matches = relationship('CandidateMatch', backref='opportunity')

    def to_dict(self, include_matches=False):
        data = {
            'id': self.id,
            'client_company': self.client_company,
            'opportunity_type': self.opportunity_type,
            'tech_stack': self.tech_stack,
            'project_duration': self.project_duration,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'location': self.location,
            'remote_status': self.remote_status,
            'resources_count': self.resources_count,
            'seniority_levels': self.seniority_levels,
            'required_certs': self.required_certs,
            'competition_status': self.competition_status,
            'opportunity_source': self.opportunity_source,
            'sales_stage': self.sales_stage,
            'probability': self.probability,
            'created_date': self.created_date.isoformat(),
            'sales_rep_id': self.sales_rep_id
        }
        
        if include_matches and self.candidate_matches:
            data['candidate_matches'] = [match.to_dict() for match in self.candidate_matches]
            
        return data 