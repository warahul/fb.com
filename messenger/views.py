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


def chooseuser(request):
    username = request.POST['username']
    print username, 'in chooseuser'
    auth_user = None
    #if request.user.is_authenticated():
    auth_user = request.user
    user_msg = Messeges.objects.filter(users=auth_user).filter(users=User.objects.get(username=username))[0]
    print str(user_msg.messege)
    list1 = str(user_msg.messege).split('\0')
    list2 = [0] * len(list1)
    for i in range(0,len(list1)):
		newlist = list1[i].split('\1')
		print newlist
		list2[i] = newlist[0]
		list1[i] = newlist[1]
    mylist=zip(list1,list2)
    return render(request,'messenger/chat.html',{'sender':auth_user,'receiver':username,'mylist':mylist})
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
