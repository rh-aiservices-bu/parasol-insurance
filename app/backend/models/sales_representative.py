from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db_utils import Base

class SalesRepresentative(Base):
    __tablename__ = 'sales_representatives'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    territory = Column(String(100))
    tech_domain = Column(String(100))  # Primary technology domain specialization
    quota = Column(Float)  # Annual sales quota
    ytd_sales = Column(Float)  # Year-to-date sales
    win_rate = Column(Float)  # Historical win rate
    created_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    opportunities = relationship('Opportunity', backref='sales_rep')

    def to_dict(self, include_opportunities=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'territory': self.territory,
            'tech_domain': self.tech_domain,
            'quota': self.quota,
            'ytd_sales': self.ytd_sales,
            'win_rate': self.win_rate,
            'created_date': self.created_date.isoformat()
        }
        
        if include_opportunities and self.opportunities:
            data['opportunities'] = [opp.to_dict() for opp in self.opportunities]
            
        return data 