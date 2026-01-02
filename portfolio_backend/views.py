from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import threading


def send_contact_email(data):
    try:
        send_mail(
            subject=f"New Contact Inquiry from {data['name']}",
            message=f"""
Name: {data['name']}
Email: {data['email']}
Company: {data['company']}

Message:
{data['message']}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["syedkareemmynudeen@manovate.co.in"],
            fail_silently=True,  # 🔥 DO NOT CRASH API
        )
    except Exception as e:
        print("EMAIL ERROR:", e)


class ContactAPIView(APIView):
    def post(self, request):
        data = request.data

        if not data.get("name") or not data.get("email") or not data.get("message"):
            return Response(
                {"error": "Required fields missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Send email in background (NON-BLOCKING)
        threading.Thread(
            target=send_contact_email,
            args=(data,),
            daemon=True
        ).start()

        # ✅ ALWAYS return success to frontend
        return Response(
            {
                "success": True,
                "message": "Contact request received"
            },
            status=status.HTTP_201_CREATED
        )
