from django.urls import path
from . import api

urlpatterns = [
    path('login/', api.LoginAPIView.as_view(), name='login'),
    path('logout/', api.LogoutAPIView.as_view(), name='logout'),
    path('validate-token/', api.ValidateTokenAPIView.as_view(), name='validate_token'),
    path('process/', api.AbstractInputAPIView.as_view(), name="process"),
    path('logs/', api.ListAllLogsAPIView.as_view(), name="logs"),
    path('log/<id>', api.LogAPIView.as_view(), name="log"),
    path('create/', api.CreateLogsAPIView.as_view(), name="create"),
    path('delete-log/', api.DeleteLogAPIView.as_view(), name="delete"),
]