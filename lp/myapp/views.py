from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from pymongo import MongoClient
import logging
logger = logging.getLogger(__name__)
    
client = MongoClient('mongodb://localhost:27017/')
db = client['lp']
users_collection = db['User']

def home(request):
    return render(request,"myapp/myapphome.html")

@csrf_protect
def login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user1 = users_collection.find_one({'username':username})
        if user1 and check_password(password,user1['password']):
            request.session['username'] = username
            data = users_collection.find_one({'username':username})
            context = {'data':data}
            return render(request,'myapp/myappadmin.html',context)
        else:
            error_message = 'Username or password incorrect!'
    return render(request,'myapp/myapplogin.html',{'error_message':error_message})

@csrf_protect
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if users_collection.find_one({'username': username}):
            return render(request, 'myapp/myappsignin.html', {'error_message': 'Username already exists. Please try another username.'})
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('cnfpsswd')
        if password != confirmpassword:
            return HttpResponse("Password doesn't match")
        hashed_password = make_password(password)
        user_data = {
            'username': username,
            'name': name,
            'email': email,
            'password': hashed_password
        }
        users_collection.insert_one(user_data)
        return redirect('login')
    else:
        return render(request,"myapp/myappsignin.html")    

@login_required
def adminis(request,username):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user1 = users_collection.find_one({'username': username})
            logger.debug(f"Fetched User: {user1}")
            if user1 and check_password(password, user1['password']):
                request.session['username'] = username
                return redirect('admin_page')  # Update with your admin page URL
            else:
                error_message = 'Username or password incorrect!'
        except Exception as e:
            logger.error(f"Login Error: {e}")
            return HttpResponse(f"DatabaseError: {e}")
    return render(request, 'myapp/myapplogin.html', {'error_message': error_message})



def userlist(request):
    all_collection = users_collection.find()    
    context = {"all_users" : all_collection}
    return render(request,'myapp/myappusers.html',context)

