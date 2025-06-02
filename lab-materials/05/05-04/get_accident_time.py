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

def upload_accident_time(claim_id, accident_time):
    db.update_claim_time(claim_id, accident_time)

def get_accident_time(claim_id = None):
    claim_info = db.get_claim_info(claim_id)
    claim_body = claim_info["body"]
    
    with open('templates/time_template.txt') as f:
        template = f.read()
    
    accident_time = infer_with_template(claim_body, template)
    print(accident_time)
    upload_accident_time(claim_id, accident_time)
    
    
def batch_get_accident_time(claim_ids = None):
    if not claim_ids:
        with open('claims.json') as f:
            claim_ids = json.load(f)["claim_ids"]
            
    print(f"processing claims: {claim_ids}")
    
    for claim_id in claim_ids:
        get_accident_time(claim_id)
    
if __name__ == '__main__':
    sentiment = batch_get_accident_time()