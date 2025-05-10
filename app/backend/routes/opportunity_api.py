from flask import Blueprint, jsonify, request, current_app
from app.backend.models.opportunity import Opportunity
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.services.opportunity_analysis import OpportunityAnalysisService
from app.backend.db_utils import db

opportunity_bp = Blueprint('opportunity', __name__)

@opportunity_bp.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    """Get list of opportunities with filtering"""
    sales_rep_id = request.args.get('sales_rep_id')
    stage = request.args.get('stage')
    client = request.args.get('client')
    tech = request.args.get('tech')
    
    query = Opportunity.query
    
    if sales_rep_id:
        query = query.filter(Opportunity.sales_rep_id == sales_rep_id)
    if stage:
        query = query.filter(Opportunity.sales_stage == stage)
    if client:
        query = query.filter(Opportunity.client_company.ilike(f'%{client}%'))
    if tech:
        query = query.filter(Opportunity.tech_stack.ilike(f'%{tech}%'))
        
    opportunities = query.order_by(Opportunity.created_date.desc()).all()
    return jsonify([opportunity.to_dict() for opportunity in opportunities])

@opportunity_bp.route('/api/opportunities/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    """Get detailed information about a specific opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    return jsonify(opportunity.to_dict(include_matches=True))

@opportunity_bp.route('/api/opportunities', methods=['POST'])
def create_opportunity():
    """Create a new opportunity"""
    data = request.get_json()
    
    opportunity = Opportunity(
        client_company=data['client_company'],
        opportunity_type=data['opportunity_type'],
        tech_stack=data.get('tech_stack'),
        project_duration=data.get('project_duration'),
        budget_min=data.get('budget_min'),
        budget_max=data.get('budget_max'),
        start_date=data.get('start_date'),
        location=data.get('location'),
        remote_status=data.get('remote_status'),
        resources_count=data.get('resources_count'),
        seniority_levels=data.get('seniority_levels'),
        required_certs=data.get('required_certs'),
        competition_status=data.get('competition_status'),
        opportunity_source=data.get('opportunity_source'),
        sales_stage=data.get('sales_stage', 'Initial Contact'),
        probability=data.get('probability', 0.0),
        sales_rep_id=data.get('sales_rep_id')
    )
    
    db.session.add(opportunity)
    db.session.commit()
    
    return jsonify(opportunity.to_dict()), 201

@opportunity_bp.route('/api/opportunities/<int:opportunity_id>', methods=['PUT'])
def update_opportunity(opportunity_id):
    """Update an existing opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(opportunity, key):
            setattr(opportunity, key, value)
    
    db.session.commit()
    return jsonify(opportunity.to_dict())

@opportunity_bp.route('/api/opportunities/<int:opportunity_id>/analyze', methods=['GET'])
def analyze_opportunity(opportunity_id):
    """Run opportunity analysis"""
    analysis_service = OpportunityAnalysisService(
        nlp_model=current_app.nlp_model,
        qualification_model=current_app.qualification_model,
        matching_model=current_app.matching_model
    )
    
    analysis_result = analysis_service.analyze_opportunity(opportunity_id)
    return jsonify(analysis_result)

@opportunity_bp.route('/api/opportunities/<int:opportunity_id>/candidates', methods=['GET'])
def get_matching_candidates(opportunity_id):
    """Get candidates matching an opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    matches = CandidateMatch.query.filter_by(opportunity_id=opportunity_id)\
        .order_by(CandidateMatch.match_score.desc()).all()
        
    candidates = [match.candidate.to_dict(include_match_details=True) for match in matches]
    return jsonify(candidates)

@opportunity_bp.route('/api/opportunities/<int:opportunity_id>/candidates/<int:candidate_id>/match', methods=['POST'])
def create_candidate_match(opportunity_id, candidate_id):
    """Create a new candidate match for an opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    candidate = Candidate.query.get_or_404(candidate_id)
    
    data = request.get_json()
    
    match = CandidateMatch(
        opportunity_id=opportunity_id,
        candidate_id=candidate_id,
        match_score=data.get('match_score'),
        skill_match_pct=data.get('skill_match_pct'),
        rate_match_pct=data.get('rate_match_pct'),
        availability_match=data.get('availability_match'),
        notes=data.get('notes')
    )
    
    db.session.add(match)
    db.session.commit()
    
    return jsonify(match.to_dict()), 201 