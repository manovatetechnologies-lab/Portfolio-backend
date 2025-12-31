from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ContactAPIView(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            email = request.data.get("email")
            company = request.data.get("company")
            message = request.data.get("message")

            if not name or not email or not message:
                return Response(
                    {"error": "Required fields missing"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 🔥 NO EMAIL. JUST RETURN SUCCESS.
            return Response(
                {
                    "success": True,
                    "message": "Backend is working correctly"
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
