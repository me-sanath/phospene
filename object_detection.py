import cv2
import torch
import requests
from torchvision import transforms
from ultralytics import YOLO

# Load the YOLOv5 model (pre-trained on COCO dataset)
model = YOLO("yolov5s.pt")  # Replace 'yolov5s.pt' with the desired YOLO model (e.g., yolov5m.pt)

# Define the endpoint URL for sending data
ENDPOINT_URL = "http://your-server-endpoint.com/data"

def send_data_to_endpoint(data):
    try:
        response = requests.post(ENDPOINT_URL, json=data)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    # Open a connection to the camera
    cap = cv2.VideoCapture(0)  # Change the index if you have multiple cameras

    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    print("Press 'q' to quit the application.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Run YOLO model on the frame
        results = model.predict(source=frame, conf=0.5, save=False, verbose=False)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                label = model.names[box.cls[0].item()]

                # Draw the bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Put the label and confidence score
                label_text = f"{label} {conf:.2f}"
                cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Check for specific labels (e.g., 'person' or potential hazards)
                if label in ["person", "knife", "scissors"]:  # Add other labels as needed
                    data = {
                        "label": label,
                        "confidence": conf,
                        "bounding_box": {
                            "x1": x1, "y1": y1, "x2": x2, "y2": y2
                        }
                    }
                    print(data)
                    # send_data_to_endpoint(data)

        # Display the resulting frame
        cv2.imshow('Object Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
