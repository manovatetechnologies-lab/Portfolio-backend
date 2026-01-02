from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import traceback


class ContactAPIView(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            email = request.data.get("email")
            company = request.data.get("company")
            message = request.data.get("message")

            print("📩 Incoming contact request")
            print("Name:", name)
            print("Email:", email)
            print("Company:", company)
            print("Message:", message)

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

            return Response(
                {"success": True},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print("❌ ERROR OCCURRED")
            traceback.print_exc()   # 🔥 THIS IS THE KEY LINE

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
