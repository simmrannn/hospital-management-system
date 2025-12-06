import json

def send_email(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        recipient = body.get('recipient')
        subject = body.get('subject')
        message = body.get('message')
        
        print(f"Sending email to {recipient}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        
        # In a real app, use boto3 SES or SMTP here
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully",
                "recipient": recipient
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
