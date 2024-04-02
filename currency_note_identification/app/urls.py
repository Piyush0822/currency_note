from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name= "home"),
    path("log_in", views.log_in, name= "log_in"),
    path("register", views.register, name= "register"),
    path("dashboard", views.dashboard, name= "dashboard"),
    path("predict_by_camera", views.predict_by_camera, name= "predict_by_camera"),
    path("predict_by_file", views.predict_by_file, name= "predict_by_file"),
    path("result", views.result, name= "result"),
    path("log_out", views.log_out, name= "log_out"),
]
