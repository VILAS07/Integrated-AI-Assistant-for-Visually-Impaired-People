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
