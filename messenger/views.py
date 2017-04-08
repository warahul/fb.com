# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Users
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    template = loader.get_template('messenger/login.html')
    context = {'empty':'',}
    return HttpResponse(template.render(context, request))

def results(request,response):
                return HttpResponse(str(response))

def login(request):
    p_username = request.POST['username']
    p_password = request.POST['password']
	# ans = 0
    try:
        user = Users.objects.get(username=p_username)
        if user.password == p_password:
            return render(request,'messenger/home.html',{'user':user})
        else:
            error="Incorrect Password for username : "+p_username
    except ObjectDoesNotExist:
        error="No user with username '"+p_username+"' exists."
    return render(request,'messenger/login.html',{'error':error})

