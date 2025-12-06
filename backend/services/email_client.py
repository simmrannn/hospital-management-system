import requests
import json

EMAIL_SERVICE_URL = "http://localhost:3000/dev/send-email"

class EmailClient:
    def send_email(self, recipient, subject, message):
        """
        Calls the Serverless email service.
        """
        try:
            payload = {
                "recipient": recipient,
                "subject": subject,
                "message": message
            }
            response = requests.post(EMAIL_SERVICE_URL, json=payload)
            if response.status_code == 200:
                print(f"Email sent to {recipient}")
                return True
            else:
                print(f"Failed to send email: {response.text}")
                return False
        except Exception as e:
            print(f"Error calling email service: {e}")
            return False
