from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from uuid import uuid4
# Create your models here.
class Logs(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    prediction = models.JSONField()
    predictionTime = models.IntegerField(default=0)
    note = models.TextField()
    timeStamp = models.DateTimeField()
    
class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'