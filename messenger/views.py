# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Messeges
from .models import Seen
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
import string, json
# Create your views here.
def index(request):
    return render(request, 'messenger/login.html')

def results(request,response):
                return HttpResponse(str(response))

def Sitelogin(request):
    if request.method =="POST":
        p_username = request.POST['username']
        p_password = request.POST['password']

        user = authenticate(username=p_username, password=p_password)

        if user is not None:
            login(request, user)
            return render(request,'messenger/home.html',{'user':user})
        else:
            error="Incorrect Username/Password"
            return render(request,'messenger/login.html',{'error':error})
    else:
        if request.user.is_authenticated():
            return render(request,'messenger/home.html')
        else:
            return render(request,'messenger/login.html')

def SignUp(request):
    if request.method == "POST":
        p_username = request.POST['username']
        p_password = request.POST['password']
        try:
            user= User.objects.get(username=p_username)
            info="Username :"+ p_username+" Exists. "
            return render(request,'messenger/signup.html',{'info':info})
        except User.DoesNotExist:
            info="Username :"+p_username+" successfully Create. "
            User.objects.create_user(username=p_username,password=p_password)
            return render(request,'messenger/signup.html',{'info':info})

    else:
        return render(request,'messenger/signup.html')

def chooseuser(request):
    usernames = request.POST['username']
    auth_user = None
    #if request.user.is_authenticated():
    auth_user = request.user
    #user_msg = Messeges.objects.filter(users=auth_user)
    user_msgs = Messeges.objects.filter(users=auth_user).filter(users__username__startswith=usernames)
    options = []
    ids = []
    for user_msg in user_msgs:
        options.append(user_msg.users.all())
        ids.append(user_msg.id)
    #print '@@@',dir(user_msg[0]),user_msg[0].id,user_msg[0].users.all(),user_msg[0].messege
    #for user in usernames.split(','):
    #    if user_msg:
    #        user_msg=user_msg.filter(users=User.objects.get(username=user))

    #list1=[];
    #list2=[];
    #noMsgSent=0;
    #beginCount=0;
    #endCount=0;
    #if user_msg :
    #    user_msg=user_msg[0]
    #    list1 = str(user_msg.messege).split('\0')
    #    list2 = [0] * len(list1)
    #    if len(list1)>10 :
    #        noMsgSent=10;
    #    else:
    #        noMsgSent=len(list1)
    #    for i in range(len(list1)-noMsgSent,len(list1)):
    #        newlist = list1[i].split('\1')
    #        print (newlist)
    #        list2[i] = newlist[0]
    #        list1[i] = newlist[1]
    #    beginCount=len(list1)-noMsgSent;
    #    endCount=len(list1);

    #mylist=zip(list1[-noMsgSent:],list2[-noMsgSent:])
    return render(request,'messenger/options.html',{'zip':zip(options,ids)})
    #return render(request,'messenger/chat.html',{'sender':auth_user,'receiver':usernames,'mylist':mylist,'beginCount':beginCount,'endCount':endCount})

def openchat(request):
    print(request.POST['id-value'])
    pid = int(request.POST['id-value'])
    user_msg = Messeges.objects.get(id=pid)
    all_users = user_msg.users.all()
    auth_user = request.user
    usernames = ''
    for user in all_users:
        if user!=auth_user:
            usernames = usernames + str(user) + ","
    print (usernames)
    list1=[];
    list2=[];
    noMsgSent=0;
    beginCount=0;
    endCount=0;
    if user_msg :
        list1 = str(user_msg.messege).split('\0')
        list2 = [0] * len(list1)
        user_seen=Seen.objects.filter(curr_user=auth_user)
        all_users=user_msg.users.all()
        count=user_msg.count
        x=user_seen
        tmp=len(x)
        print(tmp)
        print(all_users)
        print(x[0].users.all())
        for j in range(0,len(all_users)):
            x=x.filter(users=all_users[j])
        tmp=len(x)
        print(tmp)
        for j in range(0,tmp):
            tmpusers=x[j].users.all()
            print(tmpusers)
            print(all_users)
            flag=0
            for user in tmpusers:
                if (user not in all_users):
                    flag=1
                    break
            if (flag==0):
                print("successly got seen")
                x=x[j]
                break
        print(len(list1))
        print(x.count)
        if len(list1)>10 :
            if (len(list1)-x.count<10):
                noMsgSent=10;
            else:
                noMsgSent=len(list1)-x.count;
        else:
            noMsgSent=len(list1)
        x.count=len(list1)
        print(x.count)
        x.save()
        for i in range(len(list1)-noMsgSent,len(list1)):
            newlist = list1[i].split('\1')
            print (newlist)
            list2[i] = newlist[0]
            list1[i] = newlist[1]
        beginCount=len(list1)-noMsgSent;
        endCount=len(list1);
        
    mylist=zip(list1[-noMsgSent:],list2[-noMsgSent:])
    return render(request,'messenger/chat.html',{'sender':auth_user,'receiver':usernames[:-1],'mylist':mylist,'beginCount':beginCount,'endCount':endCount})

def bringusers(request):
	username = request.GET['username']
	print (username)
	users = User.objects.filter(username__startswith=username)
	html = ''
	for user in users:
		if user == request.user:
			continue
		html = html + '<input type="radio" name="choose" value="'+user.username+'">'+user.username+'<br>'
	if html!='':	
		return HttpResponse(html + '<button onclick="addusers()" type="button">Add</button>')
	else:
		return HttpResponse('No users found')

def open_newchat(request):
    auth_user = request.user
    usernames = request.POST['reciever']
    user_msg = Messeges.objects.filter(users=auth_user)
    for user in usernames.split(','):
        if user_msg:
            user_msg=user_msg.filter(users=User.objects.get(username=user))
    list1=[];
    list2=[];
    noMsgSent=0;
    beginCount=0;
    endCount=0;
    if user_msg :
        tmp=len(user_msg)
        for j in range(0,tmp):
            tmpusers=user_msg[j].users.all()
            print(tmpusers)
            print(auth_user)
            flag=0
            for user in tmpusers:
                for names in username.split(','):
                    if (user==User.objects.get(username=names) or user==auth_user):
                        print(user)
                        print("shit")
                        flag=1
                        break
            if (flag==1):
                print("done")
                user_msg=user_msg[j]
                break
    if user_msg :
        list1 = str(user_msg.messege).split('\0')
        list2 = [0] * len(list1)
        if len(list1)>10 :
            noMsgSent=10;
        else:
            noMsgSent=len(list1)
        for i in range(len(list1)-noMsgSent,len(list1)):
            newlist = list1[i].split('\1')
            print (newlist)
            list2[i] = newlist[0]
            list1[i] = newlist[1]
        beginCount=len(list1)-noMsgSent;
        endCount=len(list1);
        
    mylist=zip(list1[-noMsgSent:],list2[-noMsgSent:])
    return render(request,'messenger/chat.html',{'sender':auth_user,'receiver':usernames,'mylist':mylist,'beginCount':beginCount,'endCount':endCount})

def sendMesg(request):
    new_messege=request.POST['message']
    sender=request.POST['sender']
    receivers=request.POST['receiver']
    print (new_messege, sender)
    # auth_user = None
    # if request.user.is_authenticated():
    auth_user = request.user

    user_msg=Messeges.objects.filter(users=auth_user)
    for user in receivers.split(','):
        if user_msg:
            user_msg=user_msg.filter(users=User.objects.get(username=user))

    if user_msg :
        tmp=len(user_msg)
        for j in range(0,tmp):
            tmpusers=user_msg[j].users.all()
            print(tmpusers)
            print(auth_user)
            flag=0
            for user in tmpusers:
                for names in receivers.split(','):
                    if (user==User.objects.get(username=names) or user==auth_user):
                        print(user)
                        print("shit")
                        flag=1
                        break
            if (flag==1):
                print("done")
                user_msg=user_msg[j]
                break

    # Getnotseen(request)
    print(user_msg);
    if user_msg:
        user_msg.messege=user_msg.messege+'\0'+auth_user.username+'\1'+new_messege
        user_msg.count+=1;
        user_msg.save()
        user_seen=Seen.objects.filter(curr_user=auth_user)
        all_users=user_msg.users.all()
        count=user_msg.count
        x=user_seen
        for j in range(0,len(all_users)):
            x=x.filter(users=all_users[j])
        # print(x)
        # x=x[0]
        tmp=len(x)
        for j in range(0,tmp):
            tmpusers=x[j].users.all()
            flag=0
            for user in tmpusers:
                if (user not in all_users):
                    flag=1
                    break
            if (flag==0):
                x=x[j]
                break
        x.count=count
        x.save()
    print(" printing users msg ")
    print (user_msg)
    if not user_msg :
        msg=Messeges(messege=auth_user.username+'\1'+new_messege)
        seen=Seen()
        msg.count=1;
        msg.save()
        msg.users.add(auth_user)
        for user in receivers.split(','):
            msg.users.add(User.objects.get(username=user))
        seen.curr_user=auth_user
        seen.count=1
        seen.save()
        seen.users.add(auth_user)
        for user in receivers.split(','):
            seen.users.add(User.objects.get(username=user))
        for user in receivers.split(','):
            seen=Seen()
            seen.curr_user=User.objects.get(username=user)            
            seen.count=0
            seen.save()
            for user1 in receivers.split(','):
                seen.users.add(User.objects.get(username=user1))
            seen.users.add(auth_user)
    return render(request,'messenger/home.html',{'user':auth_user})


def getMsg(request):
    usernames=request.GET['username']
    msg_beginCount=int(request.GET['beginCount'])
    msg_endCount=int(request.GET['endCount'])
    prevMsg=int(request.GET['prevMsg'])
    # auth_user = None
    # if request.user.is_authenticated():
    auth_user = request.user
    print(usernames)
    user_msg=Messeges.objects.filter(users=auth_user)
    for user in usernames.split(','):
        if user_msg:
            user_msg=user_msg.filter(users=User.objects.get(username=user))
    list1=[];
    list2=[];
    noPrevMsg=0;
    newMsg=0;
    stringToPass="";
    if user_msg:
        tmp=len(user_msg)
        for j in range(0,tmp):
            tmpusers=user_msg[j].users.all()
            print(tmpusers)
            print(usernames.split(','))
            print(auth_user)
            flag=0
            for user in tmpusers:
                for names in usernames.split(','):
                    if (user==User.objects.get(username=names) or user==auth_user):
                        print(user)
                        print("shit")
                        flag=1
                        break
            if (flag==1):
                print("done")
                user_msg=user_msg[j]
                break
        user_seen=Seen.objects.filter(curr_user=auth_user)
        all_users=user_msg.users.all()
        count=user_msg.count
        x=user_seen
        for j in range(0,len(all_users)):
            x=x.filter(users=all_users[j])
        tmp=len(x)
        for j in range(0,tmp):
            tmpusers=x[j].users.all()
            flag=0
            for user in tmpusers:
                if (user not in all_users):
                    flag=1
                    break
            if (flag==0):
                x=x[j]
                break
        list1=str(user_msg.messege).split('\0')
        print(len(list1))
        x.count=len(list1)
        if prevMsg ==1:
            print("in prevMsg")
            if msg_beginCount>10:
                noPrevMsg=10;
            else:
                noPrevMsg=msg_beginCount;

            for i in range(msg_beginCount-noPrevMsg,msg_beginCount):
                newlist = list1[i].split('\1')
                print (newlist)
                stringToPass+="<b>"+newlist[0]+":</b>  "+newlist[1]+"<br><br>";

            stringToPass+="<script>beginCount="+str(msg_beginCount-noPrevMsg)+";</script>"
            return HttpResponse(stringToPass)
        else:
            print(len(list1),msg_endCount)
            if(len(list1) > msg_endCount):
                newMsg=len(list1)-msg_endCount;

                for i in range(msg_endCount,msg_endCount+newMsg):
                    print (i,newMsg)
                    newlist = list1[i].split('\1')
                    print (newlist)
                    stringToPass+="<b>"+newlist[0]+":</b>  "+newlist[1]+"<br><br>";

                stringToPass+="<script>endCount="+str(msg_endCount+newMsg)+";</script>"
                print(stringToPass,"hellokkkk")
                return HttpResponse(stringToPass)
            else:
                return HttpResponse("")
    else:
        return HttpResponse("")

def Getnotseen(request):
    auth_user = request.user
    user_msg=Messeges.objects.filter(users=auth_user)
    user_seen=Seen.objects.filter(curr_user=auth_user)
    # print("xmen shit")
    # print(user_msg[0].users)
    # print(user_msg[1].users)
    length=len(user_msg)
    list1=[]
    print("start shit")
    for i in range(0,length):
        # print("printing user messages")
        # print(user_msg[i])
        all_users=user_msg[i].users.all()
        count=user_msg[i].count
        x=user_seen
        for j in range(0,len(all_users)):
            x=x.filter(users=all_users[j])
        # print(x)
        # x=x[0]
        tmp=len(x)
        for j in range(0,tmp):
            tmpusers=x[j].users.all()
            flag=0
            for user in tmpusers:
                if (user not in all_users):
                    flag=1
                    break
            if (flag==0):
                x=x[j]
                break
        if (x.count!=count):
            list1.append((user_msg[i],x.count))
            x.count=user_msg[i].count
            x.save()

    print("end shit")
    stringToPass=""
    usernames=""
    for i in range(0,len(list1)):
        list2=str(list1[i][0].messege).split('\0')
        if (len(list2) > list1[i][1]):
            for user in all_users:
                if user!=auth_user:
                    usernames = usernames + str(user) + ","
            stringToPass+='<input type="radio" name="id-value" value="'+str(list1[i][0].id)+'" >'+ usernames +'<br><hr>'
    

    print("printing ss",stringToPass)

    return HttpResponse(stringToPass)
