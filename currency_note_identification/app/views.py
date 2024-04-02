from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.verify import authentication
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from datetime import datetime
from .form import currency_form
from .process import currency_prediction, currency_prediction_file
from .models import currency_data
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image

font = cv2.FONT_HERSHEY_SIMPLEX
# Create your views here.
def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    # return HttpResponse("This is Home page")    
    return render(request, "log_in.html")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
    # return HttpResponse("This is Home page")    
    return render(request, "register.html")


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'fname': request.user.first_name,
        'form' : currency_form()
        }
    return render(request, "dashboard.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def predict_by_camera(request):
    context = {
        'fname': request.user.first_name,
        'form' : currency_form()
        }
    if request.method == "POST":
        # Define the image dimensions and number of classes
        img_width, img_height = 224, 224
        num_classes = 9

        # Open the video capture device
        capture = cv2.VideoCapture(0)
        
        while True:
            ret, frame = capture.read()
            frame = cv2.resize(frame, (900, 600))

            # If camera not started
            if not ret:
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (img_width, img_height))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img /= 255.
            # Use your model to predict the class of the uploaded image
            pred = currency_prediction(img)
            cv2.rectangle(frame, (0, 0), (900, 40), (0, 0, 0), -1)
            cv2.putText(frame, "Prediction:" + str(pred), (20, 30), font, 1, (255, 255, 0), 2)
            
            
            
            if cv2.waitKey(33) & 0xFF == ord('q'):
                return redirect('log_out')
            cv2.imshow('Video', frame)

        capture.release()
        cv2.destroyAllWindows()

        
            
    return render(request, "predict_by_camera.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def predict_by_file(request):
    context = {
        'fname': request.user.first_name,
        'form' : currency_form()
        }
    if request.method == "POST":
        form = currency_form(request.POST, request.FILES)
        if form.is_valid():
            currency_note = form.cleaned_data['currency_note']
            pred = currency_prediction_file(currency_note)
            currency_data_save = currency_data(uploaded_note = currency_note, pred = pred)
            currency_data_save.save()
            if pred == 'Fake':
                messages.error(request, "Fake Currency Detected")
                return redirect("result")
            elif pred == 'Not_Detected':
                messages.error(request, "Currency Not Detected")
                return redirect("result")
            else:
                messages.success(request, "Original Currency Detected")
                return redirect("result")   
        else:
            messages.error(request, "Invalid Form")
            return redirect("predict_by_file")
    return render(request, "predict_by_file.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def result(request):
    currency = currency_data.objects.last()
    context = {
        'fname': request.user.first_name,
        'currency' : currency
        }
    
    return render(request, "result.html",context)
