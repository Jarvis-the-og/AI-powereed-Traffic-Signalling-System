import cv2
import numpy as np
import requests
import time
import os

# Load YOLO model
try:
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = f.read().strip().split("\n")
    layer_names = net.getUnconnectedOutLayersNames()
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit(1)

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit(1)

# ESP32 settings
ESP32_IP = "http://192.168.43.215/vehicle_count"
last_send_time = time.time()
send_interval = 1.0  # Send data every 1 second

# Function to clear console based on OS
def clear_console():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Unix/Linux/MacOS
    else:
        _ = os.system('clear')

print("Vehicle detection system started")

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            continue

        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        detections = net.forward(layer_names)
        
        vehicle_count = 0
        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                # Detect vehicles (Car = 2, Motorcycle = 3, Bus = 5, Truck = 7)
                if confidence > 0.7 and class_id in [2, 3, 5, 7]:
                    vehicle_count += 1
                    center_x = int(obj[0] * width)
                    center_y = int(obj[1] * height)
                    w = int(obj[2] * width)
                    h = int(obj[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    # Draw detection box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    label = f"{classes[class_id]}: {round(confidence * 100, 2)}%"
                    cv2.putText(frame, label, (x, y - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Clear console before printing new info
        clear_console()
        
        # Display count with timestamp
        current_time = time.strftime("%H:%M:%S")
        print(f"\n=== Vehicle Detection Status [{current_time}] ===")
        print(f"Current Vehicle Count: {vehicle_count}")
        print("Status: Running")
        print("Press 'q' to quit")
        print("=====================================\n")
        
        # Display count on frame
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Real-Time Vehicle Detection", frame)
        
        # Send data to ESP32 at intervals
        current_time = time.time()
        if current_time - last_send_time >= send_interval:
            try:
                response = requests.get(f"{ESP32_IP}?count={vehicle_count}", timeout=1)
                if response.status_code == 200:
                    print(f"Data sent successfully to ESP32")
                last_send_time = current_time
            except requests.exceptions.RequestException as e:
                print(f"Failed to send data: {e}")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    except Exception as e:
        print(f"Error in main loop: {e}")
        continue

cap.release()
cv2.destroyAllWindows()