from mailjet_rest import Client
from config import Config

def send_email(email, analysis, recommendations, articles):
    mailjet = Client(auth=(Config.MJ_APIKEY_PUBLIC, Config.MJ_APIKEY_PRIVATE), version='v3.1')
    content = f"""
    Your Health Report Analysis:
    {analysis}

    Recommendations:
    {recommendations}

    Relevant Articles:
    {articles}
    """
    data = {
        'Messages': [
            {
                "From": {
                    "Email": Config.EMAIL_FROM,
                    "Name": "Health Report"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": "Recipient"
                    }
                ],
                "Subject": "Your Health Report Analysis and Recommendations",
                "TextPart": content
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()
