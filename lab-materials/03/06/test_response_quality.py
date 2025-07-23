from llm_usage import infer_with_template, similarity_metric
import json


def test_response_quality():
    with open('example_text.txt') as f:
        input_text = f.read()

    with open('summary_template.txt') as f:
        template = f.read()

    expected_response = """John Smith, policy number ABC12345, reported a car accident on October 15, 2023, at 2:30 PM at the intersection of Elm Street and Maple Avenue in Springfield, Illinois. The other driver, in a Ford Escape, ran a red light and collided with Smith's Honda Accord. No serious injuries were reported, but both vehicles sustained significant damage. John has provided witness information, photos of the scene, and the other driver's details. He is requesting initiation of a claim for vehicle damages and seeks guidance on the next steps and required documentation."""

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