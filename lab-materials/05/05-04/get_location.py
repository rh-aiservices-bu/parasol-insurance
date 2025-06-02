import requests
import os
import json

import logging
from dotenv import dotenv_values, load_dotenv

from llm_usage import infer_with_template
import db_utils

# Initialize logger
logger = logging.getLogger("app")

# Get config
config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
    **dotenv_values(".pipeline-envs"), # load pipeline-specific vars
}

db = db_utils.Database(config, logger)

def upload_location(claim_id, location):
    db.update_claim_location(claim_id, location) 

def get_location(claim_id = None):    
    claim_info = db.get_claim_info(claim_id)
    claim_body = claim_info["body"]
    
    with open('templates/location_template.txt') as f:
        template = f.read()
    
    location = infer_with_template(claim_body, template)
    print(location)
    upload_location(claim_id, location)


def batch_get_location(claim_ids = None):    
    if not claim_ids:
        with open('claims.json') as f:
            claim_ids = json.load(f)["claim_ids"]
                
    print(f"processing claims: {claim_ids}")
    
    for claim_id in claim_ids:
        get_location(claim_id)
    
if __name__ == '__main__':
    location = batch_get_location()