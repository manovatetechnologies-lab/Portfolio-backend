from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import threading


def send_contact_email(name, email, company, message):
    print("📧 Attempting to send email...")
    print("SMTP USER:", settings.EMAIL_HOST_USER)
    print("SMTP PASS EXISTS:", bool(settings.EMAIL_HOST_PASSWORD))

    send_mail(
        subject=f"New Contact Inquiry from {name}",
        message=f"""
Name: {name}
Email: {email}
Company: {company}

Message:
{message}
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["syedkareemmynudeen@manovate.co.in"],
        fail_silently=False,
    )

    print("✅ Email sent successfully")

 
class ContactAPIView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        company = request.data.get("company")
        message = request.data.get("message")

        if not name or not email or not message:
            return Response(
                {"error": "Required fields missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 SEND EMAIL IN BACKGROUND THREAD
        threading.Thread(
            target=send_contact_email,
            args=(name, email, company, message),
            daemon=True
        ).start()

        # ✅ RESPOND IMMEDIATELY
        return Response(
            {
                "success": True,
                "message": "Contact request received"
            },
            status=status.HTTP_201_CREATED
        )
