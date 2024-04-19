""" Backend for Insurance Claims Processing App """
import hashlib
import logging
import os
import sys
import time
from typing import List
import json

import boto3
import data_classes
import db_utils
import chatbot
import httpx
from app_config import LOG_LEVELS, LOGGING_CONFIG
from dotenv import dotenv_values, load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

# Load local env vars if present
load_dotenv()

# Initialize logger
logger = logging.getLogger("app")

# Get config
config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
logger.info(f'Config: INFERENCE_SERVER_URL={config["INFERENCE_SERVER_URL"]}')

# App creation
app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)

# Initialize DB
db = db_utils.Database(config, logger)

# Initialize S3
s3 = boto3.client(
    's3',
    endpoint_url=config["S3_ENDPOINT_URL"],
    aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    use_ssl=config["S3_ENDPOINT_URL"].startswith("https"),)

# Initialize Chatbot
chatbot = chatbot.Chatbot(config, logger)

# Status API
@app.get("/health")
async def health():
    """ Basic status """
    return {"message": "Status:OK"}

@app.get("/api/db/tables")
async def db_list_tables():
    """
    List all the available tables in the Database
    """
    tables = db.list_tables()
    return tables

@app.get("/api/db/claims", response_model = List[data_classes.ClaimBaseInfo])
async def db_list_claims():
    """
    List all the claims
    """
    claims = db.list_claims()
    return claims

@app.get("/api/db/claims/{claim_id}", response_model = data_classes.ClaimFullInfo)
async def db_get_claim_info(claim_id):
    """
    Returns the full content of a claim
    """
    claim_info = db.get_claim_info(claim_id)
    return claim_info

@app.post("/api/db/claims", response_model = data_classes.ClaimBaseInfo)
async def db_create_claim(claim: data_classes.ClaimCreationInfo):
    """
    Creates a new claim
    """
    claim_id = db.create_claim(claim)
    claim_info = db.get_claim_base_info(claim_id)
    return claim_info

@app.post("/api/db/claims/{claim_id}/original_image")
async def db_upload_original_image(claim_id: int, image: UploadFile = File(...)):
    """
    Uploads an original image of a claim
    """
    # construct new filename with timestamp
    timestamp = int(time.time())
    sha256_hash = hashlib.sha256(image.filename.encode()).hexdigest()
    image_key = f"original_images/{claim_id}_{timestamp}_{sha256_hash[:8]}_{image.filename}"

    # Upload the image to S3
    s3.put_object(
        Bucket=config["IMAGES_BUCKET"],
        Key=image_key,
        Body=image.file,
    )
    # Save image info to DB
    db.upload_original_image(claim_id, image.filename, image_key)
    
    return {"message": f"{image.filename} uploaded as an original image of claim {claim_id}"}

@app.post("/api/db/claims/{claim_id}/processed_image")
async def db_upload_processed_image(claim_id: int, image: UploadFile = File(...)):
    """
    Uploads a processed image of a claim
    """
    # construct new filename with timestamp
    timestamp = int(time.time())
    sha256_hash = hashlib.sha256(image.filename.encode()).hexdigest()
    image_key = f"processed_images/{claim_id}_{timestamp}_{sha256_hash[:8]}_{image.filename}"

    # Upload the image to S3
    s3.put_object(
        Bucket=config["IMAGES_BUCKET"],
        Key=image_key,
        Body=image.file,
    )
    # Save image info to DB
    db.upload_processed_image(claim_id, image.filename, image_key)
    
    return {"message": f"{image.filename} uploaded as a processed image of claim {claim_id}"}

@app.post("/api/db/claims/{claim_id}/summary")
async def db_update_claim_summary(claim_id: int, summary: str):
    """
    Updates the summary of a claim
    """
    db.update_claim_summary(claim_id, summary)
    return {"message": "Summary uploaded"}

@app.post("/api/db/claims/{claim_id}/time")
async def db_update_claim_time(claim_id: int, time: str):
    """
    Updates the time of a claim
    """
    db.update_claim_time(claim_id, time)
    return {"message": "Time uploaded"}

@app.post("/api/db/claims/{claim_id}/location")
async def db_update_claim_location(claim_id: int, location: str):
    """
    Updates the location of a claim
    """
    db.update_claim_location(claim_id, location)
    return {"message": "Location uploaded"}

@app.post("/api/db/claims/{claim_id}/sentiment")
async def db_update_claim_sentiment(claim_id: int, sentiment: str):
    """
    Updates the sentiment of a claim
    """
    db.update_claim_sentiment(claim_id, sentiment)
    return {"message": "Sentiment uploaded"}

@app.get("/api/images")
async def s3_list_images():
    """
    Returns the list of images
    """
    images = s3.list_objects(Bucket=config["IMAGES_BUCKET"])
    return images

@app.get("/api/images/{image_key:path}")
async def s3_get_image(image_key: str):
    """
    Returns the image with the given key
    """
    image = s3.get_object(Bucket=config["IMAGES_BUCKET"], Key=image_key)
    return StreamingResponse(image["Body"], media_type=image["ContentType"])

@app.websocket("/ws/query")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        for next_item in chatbot.stream(data["query"], data["claim"]):
            answer = json.dumps(next_item)
            await websocket.send_text(answer)

# Serve React App
class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        if len(sys.argv) > 1 and sys.argv[1] == "dev":
            # We are in Dev mode, proxy to the React dev server
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://localhost:9000/{path}")
            return Response(response.text, status_code=response.status_code)
        else:
            try:
                return await super().get_response(path, scope)
            except (HTTPException, StarletteHTTPException) as ex:
                if ex.status_code == 404:
                    return await super().get_response("index.html", scope)
                else:
                    raise ex

app.mount("/", SPAStaticFiles(directory="public", html=True), name="spa-static-files")

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
