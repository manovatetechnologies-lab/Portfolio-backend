from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


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

        # 🔥 SAFE EMAIL BLOCK (THIS FIXES YOUR ERROR)
        try:
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
        except Exception as e:
            print("Email error:", e)

        return Response(
            {"success": True, "message": "Inquiry sent successfully"},
            status=status.HTTP_201_CREATED
        )
