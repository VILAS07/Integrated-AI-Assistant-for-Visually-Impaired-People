# Integrated-AI-Assistant-for-Visually-Impaired-People

A comprehensive AI assistant designed to help visually impaired people with face recognition, object detection, text recognition, and emergency alerts.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Webcam
- Microphone
- Speakers

### Installation
1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

#### 1. Environment Variables
Create a `.env` file in the root directory with the following variables:

**Cohere API Key (for AI functionality):**
```
COHERE_API_KEY=your_cohere_api_key_here
```
Get your API key from: https://console.cohere.ai/

**Twilio Credentials (for emergency alerts):**
```
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
EMERGENCY_CONTACT=your_emergency_contact_phone_number_here
```
Get these credentials from: https://console.twilio.com/

#### 2. Download Model Files
Download the required YOLO model files and place them in the root directory:
- `yolo11n.pt` (5.4MB) - Lightweight object detection
- `yolo11l.pt` (49MB) - Large object detection model  
- `yolov8m.pt` (50MB) - Medium YOLOv8 model

You can download these from the official Ultralytics repository or use:
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolo11n.pt
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolo11l.pt
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt
```

### Usage
Run the main application:
```bash
python AI.py
```

### Features
- **Face Recognition**: Save and recognize faces
- **Object Detection**: Detect objects and estimate distance
- **Text Recognition**: Read text from camera
- **Emergency Alerts**: Send SMS and make calls in emergencies
- **Voice Commands**: Control everything with voice

### Voice Commands
- "activate face" - Start face recognition
- "activate object" - Start object detection  
- "activate text" - Start text recognition
- "help" - Trigger emergency alert
- "stop" - Stop current operation

## Project Structure
```
├── AI.py              # Main application file
├── face.py            # Face recognition module
├── object.py          # Object detection module
├── text.py            # Text recognition module
├── emergency.py       # Emergency alert system
├── dataset/           # Face dataset directory
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License.
