from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
import os

load_dotenv()  

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
EMERGENCY_CONTACT = os.getenv("EMERGENCY_CONTACT")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_emergency_sms():
    try:
        message = client.messages.create(
            body="Emergency Alert: This is an automated call from a blind assistance app. Please assist immediately.",
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_CONTACT
        )
        return True, f"SMS sent successfully to {EMERGENCY_CONTACT} (SID: {message.sid})"
    except TwilioRestException as e:
        print(f"SMS Error: {str(e)}")
        return False, f"Failed to send SMS: {str(e)}"

def make_emergency_call():
    try:
        call = client.calls.create(
            twiml="<Response><Say voice='alice'>Emergency alert. This is an automated call from a blind assistance app. Please assist immediately.</Say></Response>",
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_CONTACT
        )
        return True, f"Call initiated successfully to {EMERGENCY_CONTACT} (SID: {call.sid})"
    except TwilioRestException as e:
        print(f"Call Error: {str(e)}")
        return False, f"Failed to make call: {str(e)}"

def trigger_emergency():
    sms_success, sms_message = send_emergency_sms()
    call_success, call_message = make_emergency_call()
    
    if sms_success or call_success:
        return True, f"{sms_message} | {call_message}"
    return False, f"{sms_message} | {call_message}"

if __name__ == "__main__":
    success, result = trigger_emergency()
    print(f"Emergency trigger result: {success}")
    print(f"Details: {result}")