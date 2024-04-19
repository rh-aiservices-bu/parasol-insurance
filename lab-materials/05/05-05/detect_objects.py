import os
import requests
import json
import time
import hashlib

import logging
import boto3
from dotenv import dotenv_values, load_dotenv

from process_image import process_image
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

s3 = boto3.client(
    's3',
    endpoint_url=config["DB_S3_ENDPOINT_URL"],
    aws_access_key_id=config["DB_AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config["DB_AWS_SECRET_ACCESS_KEY"],
    use_ssl=config["LLM_ENDPOINT"].startswith("https"),)

detection_endpoint = os.environ.get("detection_endpoint")

def download_images(claim_id):
    claim_info = db.get_claim_info(claim_id)
    images = claim_info["original_images"]
    
    downloaded_images = []
    failed_downloads = []

    if not images:
        return None
    
    for image in images:
        image_name = image["image_name"]
        image_key = image["image_key"]
        
        image = s3.get_object(Bucket=config["IMAGES_BUCKET"], Key=image_key)
        image_content = image["Body"].read()
        
        with open(f"{image_name}", 'wb') as file:
            file.write(image_content)

        downloaded_images.append(image_name)
        
    if failed_downloads:
        raise Exception(f"Not all images were downloaded. Successfully downloaded these: {downloaded_images}\nFailed to download these: {failed_downloads}")
        
    return downloaded_images

def upload_image(claim_id, image):
    filename = os.path.basename(image)
    timestamp = int(time.time())
    sha256_hash = hashlib.sha256(filename.encode()).hexdigest()
    image_key = f"processed_images/{claim_id}_{timestamp}_{sha256_hash[:8]}_{filename}"
    # Upload the image to S3
    s3.put_object(
        Bucket=config["IMAGES_BUCKET"],
        Key=image_key,
        Body=open(image, 'rb'),
    )
    # Save image info to DB
    db.upload_processed_image(claim_id, filename, image_key)

def upload_images(claim_id, images):    
    for image in images:
        upload_image(claim_id, image)
        # files = {'image': (image, open(image, 'rb'), 'image/jpeg')}
        # response = requests.post(upload_endpoint, files=files)
    
def process_images(images):
    processed_images = []
    for image in images:
        processed_image = process_image(image, detection_endpoint)
        processed_images.append(processed_image)
    return processed_images

def detect_objects(claim_id = None):
    claim_id = claim_id or int(os.environ.get("claim_id"))
    
    downloaded_images = download_images(claim_id)
    if not downloaded_images:
        print(f"skipping claim {claim_id} as there were no images attached")
        return
    processed_images = process_images(downloaded_images)
    upload_images(claim_id, processed_images)

def batch_detect_objects(claim_ids = None):
    if not claim_ids:
        with open('claims.json') as f:
            claim_ids = json.load(f)["claim_ids"]
            
    print(f"processing claims: {claim_ids}")
    
    for claim_id in claim_ids:
        detect_objects(claim_id)

if __name__ == '__main__':
    batch_detect_objects()