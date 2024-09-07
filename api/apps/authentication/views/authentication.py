# from rest_framework import permissions, views
# from rest_framework.response import Response

# from api.apps.authentication.permissions import IsClientUser


# class MyView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         client_id = request.auth.get("client_id")

#         return Response({"message": f"Your client_id is {client_id}"})
