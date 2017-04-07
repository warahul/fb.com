# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Users
from django.urls import reverse

# Create your views here.
def index(request):
    template = loader.get_template('messenger/index.html')
    context = {'empty':'',}
    return HttpResponse(template.render(context, request))

def results(request,response):
                return HttpResponse(str(response))

def login(request):
	p_username = request.POST['username']
	p_password = request.POST['password']
	ans = 0
	users_list = Users.objects.all()
	for u in users_list:
		if u.username==p_username and u.password==p_password:
			ans = 1
	return HttpResponseRedirect(reverse('messenger:results', args=(ans,)))

