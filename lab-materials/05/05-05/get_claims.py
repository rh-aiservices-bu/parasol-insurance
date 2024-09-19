import os
import requests
import json

import logging
from dotenv import dotenv_values, load_dotenv

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

def get_unprocessed_claims():
    claims_info = db.list_claims()
    
    unprocessed_list = []
    for claim in claims_info:
        if not claim["summary"]:
            unprocessed_list.append(claim["id"])
    print(f"Found unprocessed claims: {unprocessed_list}")
    return unprocessed_list

def get_claims(claim_ids=None):
    claim_ids = claim_ids or int(os.environ.get("claim_id"))
    
    if not claim_ids:
        logger.info("Getting unprocessed claims")
        claim_ids = get_unprocessed_claims()
    else:
        logger.info(f"Using claim {claim_ids}")
        claim_ids = [claim_ids]
        
    with open('claims.json', 'w') as f:
        json.dump({
            "claim_ids": claim_ids,
        }, f)
    
    print(f"Will process claims: {claim_ids}")
    return claim_ids
        
if __name__ == '__main__':
    get_claims()