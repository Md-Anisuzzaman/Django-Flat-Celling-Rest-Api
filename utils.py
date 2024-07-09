from rest_framework.response import Response
from datetime import datetime, timedelta, timezone
from functools import wraps
from django.http import JsonResponse
import jwt


def get_tokens(user):  # Make sure to include 'self' as the first parameter
    # Define your payload
    payload = {
        'email': user['email'],
        'password': user['password']
        # Add any other user-related information you want to include in the token
    }
    # Set expiration time in minutes
    access_token_exp = datetime.now(timezone.utc) + timedelta(minutes=1)
    refresh_token_exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    # Encode the JWT token with the expiration time
    access_token = jwt.encode({'exp': access_token_exp, **payload},
                              'secret_key', algorithm='HS256')
    refresh_token = jwt.encode({'exp': refresh_token_exp, **payload},
                               'secret_key', algorithm='HS256')
    token = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return token


def verify_token(token):
    try:
        jwt.decode(token, 'secret_key', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return False
    except jwt.exceptions.DecodeError:
        print("Token is not decoded")
        return False
    return True


def token_authentication_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            # Verify the access token
            is_valid_access = verify_token(access_token)
            is_valid_refresh = verify_token(refresh_token)
            if is_valid_access:
                # If token is valid, proceed with the view function
                return view_func(request, *args, **kwargs)
            elif is_valid_refresh:
                return view_func(request, *args, **kwargs)
            else:
                # If token is invalid, return an error response
                return JsonResponse({'error': 'Invalid access token'}, status=401)
        else:
            # If no access token is provided, return an error response
            return JsonResponse({'error': 'Access token is missing'}, status=401)

    return wrapper


def global_response(data=None, msg=None, status=None, errors=None):
    """
    A global function to generate consistent API responses.
    """
    response_data = {}
    if msg:
        response_data["msg"] = msg
    if data:
        response_data["data"] = data
    if errors:
        response_data["errors"] = errors

    return Response(response_data, status=status)

