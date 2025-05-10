from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.backend.db_utils import Base

class CandidateMatch(Base):
    __tablename__ = 'candidate_matches'

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    match_score = Column(Float)  # 0-100 score
    skill_match_pct = Column(Float)  # Percentage of required skills matched
    rate_match_pct = Column(Float)  # Percentage match for rate expectations
    availability_match = Column(Boolean)  # Whether candidate is available for start date
    notes = Column(Text)  # Additional notes about the match
    created_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    opportunity = relationship('Opportunity', backref='candidate_matches')
    candidate = relationship('Candidate', backref='opportunity_matches')

    def to_dict(self):
        return {
            'id': self.id,
            'opportunity_id': self.opportunity_id,
            'candidate_id': self.candidate_id,
            'match_score': self.match_score,
            'skill_match_pct': self.skill_match_pct,
            'rate_match_pct': self.rate_match_pct,
            'availability_match': self.availability_match,
            'notes': self.notes,
            'created_date': self.created_date.isoformat()
        } 