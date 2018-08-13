from django.shortcuts import render
from django.contrib.auth import authenticate , login , get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render,get_object_or_404,redirect
from .forms import Contact_form,login_page,Register_page,GuestForm,Register_Form
from django.utils.http import is_safe_url
from Guest.models import Guest
from django.http import JsonResponse,HttpResponse
from django.urls import reverse
from Guest.signals import User_logged_in
from django.views.generic import CreateView,FormView,DetailView
from ecommerce.mixins import NextUrlMixin,RequestformattachMixin
from django.contrib.messages.views import SuccessMessageMixin
