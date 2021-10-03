from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.core import serializers
from django.contrib.auth.models import User, auth
from .models import Contact
from django.db.models import Q

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect("register")
            
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect("register")

            else:
                for i in username:
                    if i.isupper():
                        messages.info(request, 'Username must be lowercase')
                        return redirect("register")

                    if i == " ":
                        messages.info(request, 'Username must not contain any Spaces')
                        return redirect("register")

                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                messages.info(request, "Account created successfully! \nLogin to continue.")
                return redirect("login")
        
        else:
            messages.info(request, "Passwords don't match!")
            return redirect("register")
    else:
        return render(request, "register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            for i in username:
                if i.isupper():
                    messages.info(request, 'Username must be lowercase')
                    return redirect("login")

            if User.objects.filter(username=username).exists():
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect("/")

                else:
                    messages.info(request, 'Invalid Credentials')
                    return redirect('login')
                
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login')

        else:
            return render(request, "login.html")

def index(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.all()
        return render(request, 'index.html', {'contacts':contacts})
    
    else:
        messages.info(request, "Please login first!")
        return redirect("login")

@csrf_exempt
def save_contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            updatedData = json.loads(request.body.decode('UTF-8'))
            name = updatedData['name']
            email = updatedData['email']

            cont = Contact.objects.filter(email=email)
            if cont.exists():
                return JsonResponse({'status':'failed', 'message':'Email address already exists!'})

            if name and email:
                con = Contact.objects.create(name=name, email=email)
                con.save()
                return JsonResponse({'status':'success', 'name':name, 'email':email, 'id':con.id})

            else:
                return JsonResponse({'status':'fail', 'message':'Missing Information!'})

        else:
            return JsonResponse({'status':'fail', 'message':'Some error occured!'})
    
    else:
        return JsonResponse({'status':'fail', 'message':'Login first!'})


def delete_contact(request, id):
    if request.user.is_authenticated:
        if Contact.objects.filter(id=id).exists():
            con = Contact.objects.get(id=id)
            con.delete()
            return JsonResponse({'status':'success'})

        else:
            return JsonResponse({'status':'fail'})

    else:
        return JsonResponse({'status':'fail', 'message':'Login first!'})



def edit_contact(request, id):
    if request.user.is_authenticated:
        if Contact.objects.filter(id=id).exists():
            con = Contact.objects.get(id=id)
            return JsonResponse({'status':'success', 'name':con.name, 'email':con.email, 'id':con.id})

        else:
            return JsonResponse({'status':'fail'})

    else:
        return JsonResponse({'status':'fail', 'message':'Login first!'})


@csrf_exempt
def edit(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':

            updatedData = json.loads(request.body.decode('UTF-8'))
            name = updatedData['name']
            email = updatedData['email']

            con = Contact.objects.filter(id=id)
            if con.exists():
                con = con.first()

                cont = Contact.objects.filter(email=email)
                if cont.exists():
                    for c in cont:
                        if not c.id == con.id:
                            return JsonResponse({'status':'fail', 'message':'Email address already exists!'})

                if name and email:
                    con.name = name
                    con.email = email
                    con.save()
                    return JsonResponse({'status':'success', 'name':name, 'email':email, 'id':con.id})

                else:
                    return JsonResponse({'status':'fail', 'message':'Missing Information!'})

            else:
                return JsonResponse({'status':'fail', 'message':'User does not exist!'})


        else:
            return JsonResponse({'status':'fail', 'message':'Some error occured!'})
    
    else:
        return JsonResponse({'status':'fail', 'message':'Login first!'})


def search(request, page):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['name']
            start = (page * 10) - 10
            end = (page * 10)
            if name:
                more = None
                contacts = Contact.objects.filter(Q(name__icontains=name) | Q(email__icontains=name))[start:end]
                if contacts.count() >= 10:
                    more = "yes"
                if contacts.exists():
                    return render(request, "search.html", {'exist':'yes', 'contacts':contacts, 'name':name, 'next':(page+1), 'more':more})
                else:
                    return render(request, "search.html", {'exist':None})
            else:
                return render(request, "search.html", {'exist':None})
        
        else:
            return redirect('/')
    
    else:
        messages.info(request, "Login first!")
        return redirect("login")