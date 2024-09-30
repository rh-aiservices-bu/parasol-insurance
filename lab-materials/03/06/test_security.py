import os
import requests
import json

def test_security(endpoint, expected_id,):
    response = requests.get(endpoint)

    if response.status_code==200:
        response_json = response.json()
    else:
        raise Exception(f"Response status code is {response.status_code}")

    if expected_id not in response_json["data"][0]["permission"][0]["id"]:
        raise Exception(f"Model ID has changed, model may have been tampered with")

    print(f"Security check OK")

    with open("security_result.json", "w") as f:
        json.dump({
            "model_id_match": expected_id in response_json["data"][0]["permission"][0]["id"],
        }, f)

if __name__ == '__main__':
    info_endpoint = "http://granite-7b-instruct-predictor.ic-shared-llm.svc.cluster.local:8080" + "/v1/models"
    expected_id = "modelperm" #This is just for the demo, in a real scenario you would input the model id here
    test_security(info_endpoint, expected_id)