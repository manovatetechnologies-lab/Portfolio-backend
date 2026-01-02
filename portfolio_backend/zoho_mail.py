import requests
import os

ZOHO_TOKEN_URL = "https://accounts.zoho.in/oauth/v2/token"
ZOHO_SENDMAIL_URL = "https://mail.zoho.in/api/accounts/me/messages"

def get_access_token():
    response = requests.post(
        ZOHO_TOKEN_URL,
        data={
            "refresh_token": os.environ.get("ZOHO_REFRESH_TOKEN"),
            "client_id": os.environ.get("ZOHO_CLIENT_ID"),
            "client_secret": os.environ.get("ZOHO_CLIENT_SECRET"),
            "grant_type": "refresh_token",
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()["access_token"]


def send_zoho_mail(subject, content, to_email):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "fromAddress": "info@manovate.co.in",
        "toAddress": to_email,
        "subject": subject,
        "content": content,
    }

    response = requests.post(
        ZOHO_SENDMAIL_URL,
        headers=headers,
        json=payload,
        timeout=10
    )

    response.raise_for_status()
    return response.json()
