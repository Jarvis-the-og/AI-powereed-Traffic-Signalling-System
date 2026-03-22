# 🚦 Smart AI-Based Traffic Management System

An intelligent traffic control system that dynamically manages a 4-way intersection using **YOLOv3 vehicle detection**, **ESP32 controllers**, and **wired communication (UART)**.

---

## 📌 Overview

This project replaces traditional fixed-timer traffic signals with an **AI-driven adaptive system**.

Instead of fixed timing:
- Detects **real-time vehicle density**
- Prioritizes **high traffic lanes**
- Ensures **fair signal distribution**

---

## 🧠 System Architecture

### 🔷 High-Level Architecture

     📱 IP Camera (North)
     📱 IP Camera (South)
     📱 IP Camera (East)
     📱 IP Camera (West)
                │
                ▼
    💻 Laptop (YOLOv3 Processing)
                │
 Vehicle Count (N, S, E, W)
                │
 ┌──────────────┴──────────────┐
 ▼                             ▼
🚦 ESP32-A 🚦 ESP32-B
(North-South Control) (East-West Control)
│ │
└────────── UART ─────────────┘
│
Traffic Signal Output


---

### 🔷 Internal Workflow


Camera Feed → YOLOv3 Detection → Vehicle Counting
↓
Compare Lane Densities
↓
Select Highest Density Lane
↓
Send Decision to ESP32s
↓
Traffic Light Switching
↓
Failsafe Timer Execution


---

## ⚙️ Hardware Components

- 2 × ESP32 Development Boards  
- 4 × Smartphones (IP Webcam)  
- LEDs (Red, Yellow, Green) or Relay Modules  
- Resistors (1kΩ)  
- Breadboard & Jumper Wires  
- Laptop (for YOLOv3 processing)  

---

## 🔌 Circuit Diagram (LED Example)


ESP32 GPIO (D5 / GPIO5)
│
[1kΩ Resistor]
│
LED (+)
│
LED (-)
│
GND


---

## 🔗 ESP32 Communication (UART)


ESP32-A ESP32-B

TX (GPIO17) -------> RX (GPIO16)
RX (GPIO16) <------- TX (GPIO17)
GND ------- GND


---

## 💻 Software Stack

### 🖥️ Laptop:
- Python  
- OpenCV  
- YOLOv3  

### 📡 ESP32:
- Arduino IDE  
- UART Communication  
- Optional: Blynk  

---

## 🚀 Features

- 📊 Real-time vehicle detection using YOLOv3  
- 🚦 Dynamic traffic signal control  
- ⚡ Wired ESP32 communication (low latency)  
- ⚖️ Fairness system (anti-starvation logic)  
- 📱 Low-cost IP camera setup using phones  

---

## 🧩 Working Algorithm

1. Capture video from 4 IP cameras  
2. Run YOLOv3 on laptop  
3. Detect and count vehicles per lane  
4. Send vehicle count to ESP32s  
5. Compare densities  
6. Lane with highest density → GREEN signal  
7. Others remain RED  

### ⏱️ Failsafe:
- Every 5 minutes → all lanes get **15 sec GREEN**

---

## 📡 Communication Format

Example data sent from laptop:


N:12,S:8,E:20,W:5


---

## 🔧 ESP32 Sample Code

```cpp
#define LED_PIN 5

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    int value = Serial.parseInt();
    digitalWrite(LED_PIN, value);
  }
}
🧠 YOLO Processing Flow
Frame Capture → Preprocessing → YOLOv3 Model
        ↓
Vehicle Detection (Bounding Boxes)
        ↓
Vehicle Count per Lane
        ↓
Send Data to ESP32
📈 Future Enhancements
🚑 Emergency vehicle detection (ambulance priority)
📡 Cloud dashboard for monitoring
📍 Google Maps traffic integration
🤖 Predictive traffic AI
📲 Mobile control system
⚠️ Challenges
Real-time YOLO performance
Stable IP camera streaming
ESP32 synchronization
Environmental conditions (lighting, rain)
🌍 Use Cases
Smart Cities
Traffic Optimization Systems
AI Research Projects
Autonomous Infrastructure
👨‍💻 Author

Rishabh Dev Pandey
B.Tech CSE
SRM Institute of Science and Technology

⭐ Support

If you like this project:

⭐ Star the repo
🔁 Share it
🤝 Contribute
