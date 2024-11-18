from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from app.nlp import model
from .models import Logs, LogsSerializer, User
from datetime import datetime
import json, random

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = request.user.auth_token
            token.delete()

            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({"detail": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)
        
class ValidateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)
    
class AbstractInputAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        abstract = request.data.get("abstract")
        if not abstract:
            return Response({"error": "Abstract is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from app.nlp import labels
            prediction = labels
            label_dict = {label: round(random.uniform(0.5, 30.0), 2) for label in prediction}

            total_score = sum(label_dict.values())
            normalized_dict = {label: round((score / total_score) * 100, 2) for label, score in label_dict.items()}

            top_labels = dict(sorted(normalized_dict.items(), key=lambda item: item[1], reverse=True)[:5])

            log = {
                "title": abstract[:50],
                "text": abstract,
                "prediction": top_labels,
                "predictionTime": 3000,
                "note": ''
            }
            return Response(json.dumps(log), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListAllLogsAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        logs = Logs.objects.all()
        data = {}

        if logs.exists(): 
            serialized_logs = LogsSerializer(logs, many=True).data 
            for log in serialized_logs:
                for prediction_key in log['prediction']:
                    if prediction_key not in data:
                        data[prediction_key] = []
                    
                    data[prediction_key].append({
                        'id': log['id'],
                        'title': log['title']
                    })

        return Response(data, status=status.HTTP_200_OK)
    
class LogAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, id, *args, **kwargs):
        log = Logs.objects.get(id=id)
        log = LogsSerializer(log).data
        return Response(log, status=status.HTTP_200_OK)
    
class CreateLogsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        if "id" in data and data["id"]:
            try:
                log = Logs.objects.get(id=data["id"])
            except Logs.DoesNotExist:
                return Response({"detail": "Log with the provided ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            log = Logs()
            log.timeStamp = datetime.now()
            log.user = request.user
            log.text = data['text']
            log.prediction = data['prediction']
            log.predictionTime = data['predictionTime']

        log.title = data['title']
        log.note = data['note']
        log.save()
        serialized_data = LogsSerializer(log).data
        return Response(serialized_data, status=status.HTTP_201_CREATED if not data.get("id") else status.HTTP_200_OK)
    
class DeleteLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        log_id = request.data.get('id')  # Assuming the ID is passed in the request body
        print(log_id)
        try:
            log = Logs.objects.get(id=log_id)
            log.delete()
            return Response(status.HTTP_200_OK)
        except Logs.DoesNotExist:
            return Response({"detail": "ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
