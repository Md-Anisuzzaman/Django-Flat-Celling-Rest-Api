from .models import UserAccount
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserCreateSerializer, UserLoginSerializer
from django.contrib.auth.hashers import check_password

from rest_framework.response import Response
from rest_framework import status
from utils import verify_token, get_tokens, global_response


class UserResistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tokens = get_tokens(request.data)
            response = Response()
            # Set cookies
            response.set_cookie(
                'access_token', str(tokens['access_token']), httponly=True)
            response.set_cookie(
                'refresh_token', str(tokens['refresh_token']), httponly=True)
            response.data = {
                "data": serializer.data,
                "token": tokens
            }
            # Return response with cookies set
            return response
        # Return error response if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        context = {
            'request': request,
            'user': request.user
        }
        serializer = UserLoginSerializer(data=request.data, context=context)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Verify the user's credentials
            try:
                user = UserAccount.objects.get(email=email)
            except UserAccount.DoesNotExist:
                # User does not exist for the provided email
                return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

            # Check password
            if check_password(password, user.password):
                # Verify tokens from cookies
                # user.last_login = timezone.now()
                access_token = request.COOKIES.get('access_token')
                refresh_token = request.COOKIES.get('refresh_token')
                access_result = verify_token(access_token)
                refresh_result = verify_token(refresh_token)

                if access_result is False:

                    if refresh_result is True:
                        response = Response()
                        # response.delete_cookie('access_token')
                        # response.delete_cookie('refresh_token')
                        tokens = get_tokens(request.data)
                        response.set_cookie(
                            'access_token', str(tokens['access_token']), httponly=True)
                        response.set_cookie(
                            'refresh_token', str(tokens['refresh_token']), httponly=True)
                        response.data = {
                            "data": serializer.data,
                            "token": tokens,
                            "message": "User login successful"
                        }
                        user.save()
                        return response
                    else:
                        # Both tokens are false, clear cookies and set new tokens
                        response = Response()
                        # response.delete_cookie('access_token')
                        # response.delete_cookie('refresh_token')
                        tokens = get_tokens(request.data)
                        response.set_cookie(
                            'access_token', str(tokens['access_token']), httponly=True)
                        response.set_cookie(
                            'refresh_token', str(tokens['refresh_token']), httponly=True)
                        response.data = {
                            "data": serializer.data,
                            "token": tokens,
                            "message": "regenerate token to login"
                        }
                        user.save()
                        return response
                else:
                    # Access token is true, user can login without resetting cookies
                    return Response({"msg": "login successfully", "data": serializer.data, }, status=status.HTTP_200_OK)
            else:
                # Password does not match
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        # Serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get(self, request, pk, format=None):
        try:
            user = UserAccount.objects.get(pk=pk)
            serializer = UserCreateSerializer(user)
            return global_response(data=serializer.data, status=status.HTTP_200_OK)
        except UserAccount.DoesNotExist:
            return global_response(msg="User not found", status=status.HTTP_404_NOT_FOUND)


class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        if role in ['Admin', 'SuperAdmin']:
            return global_response(msg="Not permitted to create User", status=status.HTTP_400_BAD_REQUEST)
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return global_response(data=serializer.data, msg="User created successfully", status=status.HTTP_200_OK)
        return global_response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    def put(self, request, pk, *args, **kwargs):
        if request.method == 'PUT':
            user = UserAccount.objects.get(pk=pk)
            serializer = UserCreateSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Save the updated data
                return global_response(data=serializer.data, msg="User updated successfully", status=status.HTTP_200_OK)
            return global_response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    def delete(self, request, pk, *args, **kwargs):
        if request.method == 'DELETE':
            try:
                user = UserAccount.objects.get(pk=pk)
                user.delete()
                return global_response(msg="User deleted successfully", status=status.HTTP_204_NO_CONTENT)
            except UserAccount.DoesNotExist:
                return global_response(errors="User not found", status=status.HTTP_404_NOT_FOUND)


class GetAllUsers(APIView):
    def get(self, request, *args, **kwargs):
        users = UserAccount.objects.all()
        serializer = UserCreateSerializer(users, many=True)
        print(serializer.data)
        return global_response(data=serializer.data, status=status.HTTP_200_OK)
