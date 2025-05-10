from flask import Blueprint, jsonify, request
from app.backend.models.candidate import Candidate
from app.backend.models.candidate_match import CandidateMatch
from app.backend.db_utils import db

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/api/candidates', methods=['GET'])
def get_candidates():
    """Get list of candidates with filtering"""
    skills = request.args.get('skills')
    location = request.args.get('location')
    availability = request.args.get('availability')
    rate_min = request.args.get('rate_min')
    rate_max = request.args.get('rate_max')
    
    query = Candidate.query
    
    if skills:
        skills_list = [s.strip() for s in skills.split(',')]
        for skill in skills_list:
            query = query.filter(Candidate.primary_skills.ilike(f'%{skill}%'))
            
    if location:
        query = query.filter(Candidate.location.ilike(f'%{location}%'))
        
    if availability:
        query = query.filter(Candidate.availability_date <= availability)
        
    if rate_min:
        query = query.filter(Candidate.hourly_rate_min >= float(rate_min))
        
    if rate_max:
        query = query.filter(Candidate.hourly_rate_max <= float(rate_max))
        
    candidates = query.order_by(Candidate.last_updated.desc()).all()
    return jsonify([candidate.to_dict() for candidate in candidates])

@candidate_bp.route('/api/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get detailed information about a specific candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify(candidate.to_dict(include_match_details=True))

@candidate_bp.route('/api/candidates', methods=['POST'])
def create_candidate():
    """Create a new candidate"""
    data = request.get_json()
    
    candidate = Candidate(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        primary_skills=data['primary_skills'],
        tech_stack=data.get('tech_stack'),
        experience_years=data.get('experience_years'),
        hourly_rate_min=data.get('hourly_rate_min'),
        hourly_rate_max=data.get('hourly_rate_max'),
        availability_date=data.get('availability_date'),
        location=data.get('location'),
        remote_preference=data.get('remote_preference'),
        certifications=data.get('certifications'),
        education=data.get('education'),
        previous_clients=data.get('previous_clients')
    )
    
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify(candidate.to_dict()), 201

@candidate_bp.route('/api/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update an existing candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(candidate, key):
            setattr(candidate, key, value)
    
    db.session.commit()
    return jsonify(candidate.to_dict())

@candidate_bp.route('/api/candidates/<int:candidate_id>/opportunities', methods=['GET'])
def get_candidate_opportunities(candidate_id):
    """Get opportunities that match a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    matches = CandidateMatch.query.filter_by(candidate_id=candidate_id)\
        .order_by(CandidateMatch.match_score.desc()).all()
        
    opportunities = [match.opportunity.to_dict() for match in matches]
    return jsonify(opportunities)

@candidate_bp.route('/api/candidates/<int:candidate_id>/availability', methods=['PUT'])
def update_candidate_availability(candidate_id):
    """Update candidate availability"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()
    
    if 'availability_date' in data:
        candidate.availability_date = data['availability_date']
    if 'remote_preference' in data:
        candidate.remote_preference = data['remote_preference']
    if 'location' in data:
        candidate.location = data['location']
        
    db.session.commit()
    return jsonify(candidate.to_dict()) 