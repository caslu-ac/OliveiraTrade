import logging
from pyexpat.errors import messages
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

import authentication
# Create your views here.
def home(request):
    return render(request, "authentication/index.html")
def signup(request):
    
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        birth_data = request.POST['birth_data']
        id = request.POST['id']
        email = request.POST['email']
        password = request.POST['password']
        passwordconfirm = request.POST['passwordconfirm']
    

        if User.objects.filter(username=username):
            messages.error(request, "o nome de usuário já está em uso")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, "este email já está cadastadro")
            return redirect('home')
        if password != passwordconfirm:
            messages.error(request, "A senha está diferente")
            return redirect('home')
        if len(id) != 12:
            messages.error(request, "Digite um CPF válido")
            return redirect('home')



        myuser = User.objects.create_user(username, email, password)
        myuser.birthdata = birth_data
        myuser.id = id
    
        myuser.save()

        messages.success(request, "Sua conta foi criada.")
    
        return redirect('signin')

    return render(request, "authentication/signup.html")
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)


        if user is not None:
            login(request, user)
            return render(request, "authentication/index.html", {'name':name})


        else: 
            messages.error(request, "usuário ou senha incorretos")

    return render(request, "authentication/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"Logout feito com sucesso")
    return redirect('home')