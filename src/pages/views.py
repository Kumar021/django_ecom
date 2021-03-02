import random
import string

import json
from django.conf import settings 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render 
from django.contrib.auth.decorators import login_required

from django.db.models import Q, Exists, Count, F, Value
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Create your views here.

def index(request):
	context = {}

	return render(request, 'pages/index.html', context)



#List Of Blogs 
def blog_list(request):

	return HttpResponse("Blog List") 


def shop(request):
	return render(request, 'pages/shop.html') 



def email(request):
    msg_html = render_to_string('email.html', {'user': request.user})
    msg_plain = render_to_string('email.txt', {'user': request.user})

    subject = 'Thank you for registering to our site'
    # message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['raj@koolbuch.com',]
    # send_mail( subject, message, email_from, recipient_list )
    send_mail(
        subject,
        msg_plain,
        email_from,
        recipient_list,
        html_message=msg_html,
    )
    return HttpResponse('redirect to a new page')