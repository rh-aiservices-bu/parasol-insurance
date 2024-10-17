from llm_usage import infer_with_template, similarity_metric
import json


def test_response_quality():
    with open('example_text.txt') as f:
        input_text = f.read()
        
    with open('summary_template.txt') as f:
        template = f.read()

    expected_response = """Dear John Smith,

Thank you for contacting XYZ Insurance Company regarding your recent car accident. We are sorry to hear about the incident and are committed to assisting you through this process.

To initiate a claim, please follow these steps:

1. Gather all necessary documentation, including the accident report (with the officer's badge number), witness contact information, photos of the accident scene, and your vehicle's repair estimate.
2. Log in to your policyholder account on our website or contact our customer service department at (800) 123-4567 to report the claim.
3. Our representative will guide you through the claim process, asking for the required information and providing you with a claim number.
4. Your insurance adjuster will be assigned to your case and will contact you to schedule an appointment to inspect the damage to your vehicle.
5. Once the assessment is complete, your adjuster will provide you with a detailed repair estimate and discuss the next steps for claim settlement.

Please note that the time it takes to process a claim can vary depending on the complexity of the accident and the amount of damage involved. We appreciate your patience and cooperation throughout this process.

If you have any questions or need further assistance, please do not hesitate to contact us at (800) 123-4567 or email us at claims@xyzinsurance.com. We are here to help.

Sincerely,

XYZ Insurance Company
Claims Department"""

    response = infer_with_template(input_text, template)
    print(f"Response: {response}")
    
    similarity = similarity_metric(response, expected_response)
    print(similarity)

    if similarity <= 0.8:
        raise Exception("Output is not similar enough to expected output")
        
    print("Response Quality OK")

    with open("quality_result.json", "w") as f:
        json.dump({
            "quality_test_response": response,
            "quality_test_similarity": similarity
        }, f)

if __name__ == '__main__':
    test_response_quality()