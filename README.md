# 🚦 Smart AI-Based Traffic Management System

> An intelligent, adaptive traffic control system for 4-way intersections — powered by **YOLOv3 real-time vehicle detection**, **dual ESP32 controllers**, and **wired UART communication**.

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Arduino](https://img.shields.io/badge/Arduino-IDE-00979D?style=flat&logo=arduino&logoColor=white)](https://arduino.cc)
[![YOLOv3](https://img.shields.io/badge/AI-YOLOv3-FF6F00?style=flat&logo=tensorflow&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

Traditional traffic signals operate on fixed timers — they can't adapt to real-world traffic. This project solves that by replacing fixed-timer signals with an **AI-driven adaptive system** that sees, decides, and responds in real time.

| Traditional System | This System |
|---|---|
| Fixed green timers | Dynamic timers based on live density |
| No lane awareness | Per-lane vehicle count via YOLOv3 |
| Manual reconfiguration | Fully autonomous with failsafe logic |
| High infrastructure cost | Low-cost phones as IP cameras |

---

## 🧠 System Architecture

### High-Level Overview

```
  📱 IP Camera (North)   📱 IP Camera (South)
  📱 IP Camera (East)    📱 IP Camera (West)
              │
              ▼
  ┌─────────────────────────┐
  │  💻 Laptop — YOLOv3     │  ← Real-time vehicle detection
  │  Vehicle Count: N,S,E,W │
  └────────────┬────────────┘
               │  Serial (UART)
       ┌───────┴────────┐
       ▼                ▼
  🚦 ESP32-A        🚦 ESP32-B
  (North-South)    (East-West)
       │                │
       └──── UART ──────┘
               │
    Traffic Signal Output
```

### Internal Workflow

```
Camera Feed → YOLOv3 Detection → Vehicle Count per Lane
                                        │
                              Compare Lane Densities
                                        │
                             Select Highest Density Lane
                                        │
                              Send Decision to ESP32s
                                        │
                             Traffic Light Switching
                                        │
                           Failsafe Timer Execution (5 min)
```

---

## ⚙️ Hardware Components

| Component | Quantity | Purpose |
|---|---|---|
| ESP32 Development Board | 2 | Traffic signal control |
| Smartphone (IP Webcam App) | 4 | Live camera feed per lane |
| LEDs (Red, Yellow, Green) | 12 | Signal indicators |
| 1kΩ Resistors | 12 | LED current limiting |
| Relay Module *(optional)* | 4 | Driving real traffic lights |
| Breadboard & Jumper Wires | As needed | Prototyping |
| Laptop / PC | 1 | YOLOv3 AI processing |

---

> **Note:** Always connect GND between both ESP32 boards before powering either device.

---

## 💻 Software Stack

### Laptop (AI Processing)

| Software | Role |
|---|---|
| Python 3.x | Core processing language |
| OpenCV | Camera feed capture & frame processing |
| YOLOv3 | Vehicle detection & bounding boxes |
| PySerial | Sending data to ESP32 over UART |

### ESP32 (Signal Control)

| Software | Role |
|---|---|
| Arduino IDE | Firmware development |
| HardwareSerial | UART communication between ESP32s |
| Blynk *(optional)* | Mobile monitoring dashboard |

---

## 🚀 Features

- 📊 **Real-time vehicle detection** using YOLOv3 on live camera feeds
- 🚦 **Dynamic green signal allocation** — highest-density lane gets priority
- ⚖️ **Anti-starvation logic** — ensures all lanes receive fair green time
- ⚡ **Low-latency wired UART** communication between ESP32 controllers
- 📱 **Zero-cost IP cameras** using smartphones and the IP Webcam app
- 🔧 **Modular and extensible** — easy to swap components or add new lanes

---

## 🧩 Algorithm

### Main Loop

```
1. Capture video frames from 4 IP cameras (N, S, E, W)
2. Run YOLOv3 inference on each frame
3. Count detected vehicles per lane
4. Format and send counts → ESP32 via Serial
5. ESP32 compares all lane densities
6. Lane with highest vehicle count → GREEN signal
7. All other lanes → RED signal
8. Repeat every cycle
```

### Fairness / Anti-Starvation Failsafe

```
Every 5 minutes:
  → All 4 lanes receive a mandatory 15-second GREEN phase
  → Prevents any lane from waiting indefinitely
```

---

## 📡 Communication Protocol

Data is sent from the laptop to ESP32-A over Serial in the following format:

```
N:12,S:8,E:20,W:5
```

| Field | Description |
|---|---|
| `N:12` | 12 vehicles detected on North lane |
| `S:8` | 8 vehicles on South lane |
| `E:20` | 20 vehicles on East lane *(gets GREEN)* |
| `W:5` | 5 vehicles on West lane |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install opencv-python pyserial numpy
```

Download YOLOv3 weights:
```bash
wget https://pjreddie.com/media/files/yolov3.weights -P laptop/models/
```

### Setup Steps

1. **Install the IP Webcam app** on 4 Android phones and start the server on each.
2. **Update camera IPs** in `camera_stream.py` to match your network.
3. **Flash ESP32 firmware** using Arduino IDE (`esp32_a_controller.ino` and `esp32_b_controller.ino`).
4. **Wire ESP32s** using the UART diagram above.
5. **Connect ESP32-A** to your laptop via USB.
6. **Run the system:**

```bash
cd laptop/
python main.py
```

---

## ⚠️ Known Challenges

| Challenge | Mitigation |
|---|---|
| YOLOv3 real-time performance | Use GPU acceleration or switch to YOLOv5/v8 |
| IP camera stream instability | Implement reconnect logic with timeout handling |
| Low-light detection accuracy | Tune confidence thresholds; add IR lighting |
| ESP32 UART synchronization | Use start/end delimiters in the data protocol |
| Rain / glare affecting detection | Pre-process frames with contrast normalization |

---

## 📈 Future Enhancements

- 🚑 **Emergency vehicle detection** — ambulance/fire truck gets immediate GREEN
- 📡 **Cloud monitoring dashboard** — real-time traffic stats via MQTT or Firebase
- 📍 **Google Maps integration** — reflect signal state in live traffic data
- 🤖 **Predictive AI** — use historical patterns to pre-empt congestion
- 📲 **Mobile control app** — manual override and monitoring via Blynk
- 🔊 **Pedestrian signal integration** — countdown timers for walkers

---

## 🌍 Use Cases

- Smart City Infrastructure
- Urban Traffic Optimization
- AI & IoT Research Projects
- Autonomous Infrastructure Prototypes
- College Final Year / Capstone Projects

---

## 👨‍💻 Author

**Rishabh Dev Pandey**
B.Tech — Computer Science & Engineering
SRM Institute of Science and Technology

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute with attribution.

---

## ⭐ Support

If this project helped you or inspired your work:

- ⭐ **Star** this repository
- 🔁 **Share** it with your network
- 🤝 **Contribute** via pull requests
- 🐛 **Report issues** in the Issues tab

> *Smarter signals. Smoother cities.*
