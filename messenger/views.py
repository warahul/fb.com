# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Messeges
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'messenger/login.html')

def results(request,response):
                return HttpResponse(str(response))

def Sitelogin(request):
    p_username = request.POST['username']
    p_password = request.POST['password']

    user = authenticate(username=p_username, password=p_password)

    if user is not None:
        login(request, user)
        return render(request,'messenger/home.html',{'user':user})
    else:
        error="Incorrect Username/Password"
        return render(request,'messenger/login.html',{'error':error})

def chooseuser(request):
    username = request.POST['username']
    print username, 'in chooseuser'
    auth_user = None
    #if request.user.is_authenticated():
    auth_user = request.user
    user_msg = Messeges.objects.filter(users=auth_user).filter(users=User.objects.get(username=username))[0]
    print str(user_msg.messege)
    import ast
    print ast.literal_eval(str(user_msg.messege))
    print dir(user_msg)
    return render(request,'messenger/chat.html',{'sender':auth_user,'receiver':username,'user_msg':user_msg})
    #user_msg=Messeges.objects.filter(users__in=[auth_user,User.objects.get(username=username)])[0]
    #if user_msg:
    #    user_msg.messege=user_msg.messege+","+messege
    #print(" printing users msg ")
    #print (user_msg)
    #if not user_msg :
    #    msg=Messeges(messege=messege)
    #    msg.save()
    #    msg.users.add(auth_user)
    #    msg.users.add(User.objects.get(username=username))
        #auth_user.msgList
    #return render(request,'messenger/home.html',{'user':auth_user})
    #if request.user.is_authenticated():
    #    auth_user = request.user

    #print(auth_user.msgList.all())
    #user_msg=Messeges.objects.filter(users=auth_user).filter(users=User.objects.get(username=username))[0]
    #print(user_msg);
    #if user_msg:
    #    user_msg.messege=user_msg.messege+","+messege
    #    user_msg.save()
    #print(" printing users msg ")
    #print (user_msg)
    #if not user_msg :
    #    msg=Messeges(messege=messege)
    #    msg.save()
    #    msg.users.add(auth_user)
    #    msg.users.add(User.objects.get(username=username))

    #return render(request,'messenger/home.html',{'user':auth_user})
