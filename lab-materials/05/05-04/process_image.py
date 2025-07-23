import os
import requests
from pathlib import Path

import cv2.dnn
import numpy as np

CLASSES = {
    0: "moderate",
    1: "severe"
}
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))

def preprocess(image_path):
    original_image: np.ndarray = cv2.imread(image_path)
    [height, width, _] = original_image.shape

    # Prepare a square image for inference
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image

    # Calculate scale factor
    scale = length / 640

    # Preprocess the image and prepare blob for model
    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
    return blob, scale, original_image

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    """
    Draws bounding boxes on the input image based on the provided arguments.

    Args:
        img (numpy.ndarray): The input image to draw the bounding box on.
        class_id (int): Class ID of the detected object.
        confidence (float): Confidence score of the detected object.
        x (int): X-coordinate of the top-left corner of the bounding box.
        y (int): Y-coordinate of the top-left corner of the bounding box.
        x_plus_w (int): X-coordinate of the bottom-right corner of the bounding box.
        y_plus_h (int): Y-coordinate of the bottom-right corner of the bounding box.
    """
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def postprocess(response, scale, original_image):    
    outputs = np.array([cv2.transpose(response[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    # Iterate through output to collect bounding boxes, confidence scores, and class IDs
    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.25:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2], outputs[0][i][3]]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)
    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

    detections = []

    # Iterate through NMS results to draw bounding boxes and labels
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        detection = {
            'class_id': class_ids[index],
            'class_name': CLASSES[class_ids[index]],
            'confidence': scores[index],
            'box': box,
            'scale': scale}
        detections.append(detection)
        draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                          round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))
    return original_image

def _serialize(image):
    payload = {
        'inputs': [
            {
                'name': 'images',
                'shape': [1, 3, 640, 640],
                'datatype': 'FP32',
                'data': image.flatten().tolist(),
            },
        ]
    }
    return payload

def _unpack(response_item):
    return np.array(response_item['data']).reshape(response_item['shape'])

def send_request(image, endpoint):
    payload = _serialize(image)
    
    raw_response = requests.post(f"{endpoint}/v2/models/my-first-model/infer", json = payload)
    try:
        response = raw_response.json()
    except:
        print(f'Failed to deserialize service response.\n'
              f'Status code: {raw_response.status_code}\n'
              f'Response body: {raw_response.text}')
        raise
    
    try:
        model_output = response['outputs']
    except:
        print(f'Failed to extract model output from service response.\n'
              f'Service response: {response}')
        raise

    unpacked_output = [_unpack(item) for item in model_output]
    return unpacked_output

def process_image(image_path, endpoint):
    preprocessed, scale, original_image = preprocess(image_path)
    response = send_request(preprocessed, endpoint)
    new_image = postprocess(response[0], scale, original_image)
    
    filename = os.path.basename(image_path)
    Path("processed_images").mkdir(parents=True, exist_ok=True)
    new_file_path = f"processed_images/{filename}"
    cv2.imwrite(new_file_path, new_image)
    print(f"Successfully processed image {filename}")
    
    return new_file_path

if __name__ == '__main__':
    detection_endpoint = os.environ.get("DETECTION_ENDPOINT")
    process_image("test_image.jpg", detection_endpoint)