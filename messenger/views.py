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
import string
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

def sendMesg(request):
    new_messege=request.POST['messege']
    sender=request.POST['sender']
    receivers=request.POST['receivers']
    print (new_messege, sender)
    # auth_user = None
    # if request.user.is_authenticated():
    auth_user = request.user


    user_msg=Messeges.objects.filter(users=auth_user)
    for user in receivers.split(','):
        user_msg=user_msg.filter(users=User.objects.get(username=user))

    if user_msg :
        user_msg=user_msg[0]

    print(user_msg);
    if user_msg:
        user_msg.messege=user_msg.messege+'\0'+auth_user.username+'\1'+new_messege
        user_msg.save()
    print(" printing users msg ")
    print (user_msg)
    if not user_msg :
        msg=Messeges(messege=auth_user.username+'\1'+new_messege)
        msg.save()
        msg.users.add(auth_user)
        for user in receivers.split(','):
            msg.users.add(User.objects.get(username=user))

    return render(request,'messenger/home.html',{'user':auth_user})


def getMsg(request):
    usernames=request.POST['username']
    msg_beginCount=request.POST['beginCount']
    msg_endCount=request.POST['endCount']
    prevMsg=request.POST['prevMsg']
    auth_user = None
    if request.user.is_authenticated():
        auth_user = request.user


    user_msg=Messeges.objects.filter(users=auth_user)
    for user in usernames.split(','):
        user_msg=user_msg.filter(users=User.objects.get(username=user))

    if user_msg:
        user_msg=user_msg[0]
        user_msg=str(user_msg.messege).split('\0')
        if prevMsg:
            noPrevMsg=0;
            print("in prevMsg")
            if msg_beginCount>10:
                noPrevMsg=10;
            else:
                noPrevMsg=msg_beginCount;
            split_msg=str(user_msg[msg_beginCount-noPrevMsg:msg_beginCount]).split('\1')
            return render(request,'messenger/chat.html',{'prev_msg_author':split_msg[0],'prev_msg_content':split_msg[1]})
        else:
            if(len(user_msg) > msg_endCount):
                split_msg=str(user_msg[:len(user_msg) - msg_endCount]).split('\1')
                return render(request,'messenger/chat.html',{'new_msg_author':split_msg[0],'new_msg_content':split_msg[1]})
    else:
        return render(request,'messenger/chat.html')
