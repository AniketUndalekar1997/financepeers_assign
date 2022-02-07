from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .serializers import UserSerializer, FileDataSerializer, PostSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import User, Post
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import json
from django.http import JsonResponse


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found')

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token,
            'expiry': payload['exp']
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        expiryData = {
            'expiry': payload['exp']*1000
        }

        responseData = expiryData.copy()
        responseData.update(serializer.data)

        return Response(responseData)


class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'status': 'Success'
        }
        return response


class FileUploadView(APIView):

    def post(self, request, format="json"):
        file_obj = request.FILES['file']
        file_data = file_obj.read()
        try:
            file_json = json.loads(file_data)
        except Exception:
            # print(f"excetion {traceback.format_exc()}")
            return JsonResponse({'status': "error", 'message': 'Error in json loads!'}, status=400)
        if not isinstance(file_json, list):
            return JsonResponse({'status': "error", 'message': 'Invalid Json Data!'}, status=400)

        # serilize each each_entry
        for each_entry in file_json:
            serialized_data = FileDataSerializer(data=each_entry)
            if not serialized_data.is_valid():
                return JsonResponse({'status': "error", 'message': 'Invalid Json Data!'}, status=400)

            # print(f"{serialized_data.data}")
            # print("is valid", serialized_data.is_valid())
            serialized_data.create(serialized_data.data)

        # return Response(status=200)
        return JsonResponse({'status': "success", 'message': 'File Upload Success'}, status=200)
        # do some stuff with uploaded file


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_number'
    max_page_size = 12


class ListPost(ListAPIView):
    serializer_class= PostSerializer
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination

    #this gets all the posts

