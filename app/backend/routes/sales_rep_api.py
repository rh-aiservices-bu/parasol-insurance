from flask import Blueprint, jsonify, request
from app.backend.models.sales_representative import SalesRepresentative
from app.backend.models.opportunity import Opportunity
from app.backend.db_utils import db

sales_rep_bp = Blueprint('sales_rep', __name__)

@sales_rep_bp.route('/api/sales-reps', methods=['GET'])
def get_sales_reps():
    """Get list of sales representatives with filtering"""
    territory = request.args.get('territory')
    tech_domain = request.args.get('tech_domain')
    
    query = SalesRepresentative.query
    
    if territory:
        query = query.filter(SalesRepresentative.territory.ilike(f'%{territory}%'))
    if tech_domain:
        query = query.filter(SalesRepresentative.tech_domain.ilike(f'%{tech_domain}%'))
        
    sales_reps = query.order_by(SalesRepresentative.name).all()
    return jsonify([rep.to_dict() for rep in sales_reps])

@sales_rep_bp.route('/api/sales-reps/<int:sales_rep_id>', methods=['GET'])
def get_sales_rep(sales_rep_id):
    """Get detailed information about a specific sales representative"""
    sales_rep = SalesRepresentative.query.get_or_404(sales_rep_id)
    return jsonify(sales_rep.to_dict(include_opportunities=True))

@sales_rep_bp.route('/api/sales-reps', methods=['POST'])
def create_sales_rep():
    """Create a new sales representative"""
    data = request.get_json()
    
    sales_rep = SalesRepresentative(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        territory=data.get('territory'),
        tech_domain=data.get('tech_domain'),
        quota=data.get('quota'),
        ytd_sales=data.get('ytd_sales', 0.0),
        win_rate=data.get('win_rate', 0.0)
    )
    
    db.session.add(sales_rep)
    db.session.commit()
    
    return jsonify(sales_rep.to_dict()), 201

@sales_rep_bp.route('/api/sales-reps/<int:sales_rep_id>', methods=['PUT'])
def update_sales_rep(sales_rep_id):
    """Update an existing sales representative"""
    sales_rep = SalesRepresentative.query.get_or_404(sales_rep_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(sales_rep, key):
            setattr(sales_rep, key, value)
    
    db.session.commit()
    return jsonify(sales_rep.to_dict())

@sales_rep_bp.route('/api/sales-reps/<int:sales_rep_id>/opportunities', methods=['GET'])
def get_sales_rep_opportunities(sales_rep_id):
    """Get opportunities for a sales representative"""
    sales_rep = SalesRepresentative.query.get_or_404(sales_rep_id)
    stage = request.args.get('stage')
    
    query = Opportunity.query.filter_by(sales_rep_id=sales_rep_id)
    if stage:
        query = query.filter_by(sales_stage=stage)
        
    opportunities = query.order_by(Opportunity.created_date.desc()).all()
    return jsonify([opp.to_dict() for opp in opportunities])

@sales_rep_bp.route('/api/sales-reps/<int:sales_rep_id>/performance', methods=['GET'])
def get_sales_rep_performance(sales_rep_id):
    """Get performance metrics for a sales representative"""
    sales_rep = SalesRepresentative.query.get_or_404(sales_rep_id)
    
    # Calculate additional performance metrics
    opportunities = Opportunity.query.filter_by(sales_rep_id=sales_rep_id).all()
    
    total_opportunities = len(opportunities)
    total_value = sum(opp.budget_max or 0 for opp in opportunities)
    won_opportunities = sum(1 for opp in opportunities if opp.sales_stage == 'Closed')
    active_opportunities = sum(1 for opp in opportunities if opp.sales_stage not in ['Closed', 'Lost'])
    
    return jsonify({
        'sales_rep': sales_rep.to_dict(),
        'performance': {
            'total_opportunities': total_opportunities,
            'total_value': total_value,
            'won_opportunities': won_opportunities,
            'active_opportunities': active_opportunities,
            'win_rate': (won_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0,
            'quota_achievement': (sales_rep.ytd_sales / sales_rep.quota * 100) if sales_rep.quota > 0 else 0
        }
    }) 