import os
import pyrebase  # a library for authentication using firebase
from django.contrib import messages  # Importing messages module for showing errors
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView  # Importing login and logout views
from django.contrib.messages.views import \
    SuccessMessageMixin  # Importing successmessagemixin for showing success messages
from django.http import HttpResponseRedirect  # If any error caused it will help to redirect
from django.urls import reverse  # Used in redirecting
from django.views.generic import CreateView  # class based view
from .forms import RegisterForm  # importing registration form
from typing import Any, AnyStr, Dict  # Using to define the type


firebaseConfig = {
    'apiKey':  'AIzaSyDUqTzCE50UXv5K6N8WHWA_hgTfNdUrS3c',
    'authDomain':  'talk-to-brain.firebaseapp.com',
    "databaseURL":  'https://talk-to-brain-default-rtdb.asia-southeast1.firebasedatabase.app',
    'projectId': 'talk-to-brain',
    'storageBucket': 'talk-to-brain.appspot.com',
    'messagingSenderId': '560400101460',
    'appId': '1:560400101460:web:1568a907cfeadb16b97dc1',
    'measurementId': 'G-7RZ87M8LTW',
}

firebase = pyrebase.initialize_app(firebaseConfig)  # setting the firebase config
auth = firebase.auth()  # initializing authentication using firebase


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm  # instantiating the form object
    success_message = "Please verify your mail for the best services"  # A success message
    success_url = '/'  # Success url after registration

    def form_valid(self, form: Dict[AnyStr, Any]) -> Any:  # form validations
        email = form['email'].value()  # getting the email from form object
        password = form['password1'].value()  # getting the password from form object
        try:  # some basic validation of e-mail
            user = auth.create_user_with_email_and_password(email,
                                                            password)  # create the object using e-mail and password
            login = auth.sign_in_with_email_and_password(email, password)  # login with e-mail and password`
            auth.send_email_verification(login['idToken'])  # send the verification mail to the e-mail
            return super().form_valid(form)  # calling the form object of create view
        except:
            messages.error(self.request,
                           'E-mail is already taken please enter a new e-mail')  # adding the errors in messages list which will be shown in message.html template
            return HttpResponseRedirect(reverse('users:register'))  # Redirecting to form page if there are any errors


class UserLoginView(LoginView):  # Initializing template for login view
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form['username'].value()  # getting the email from form object
        password = form['password'].value()  # getting the password from form object
        email = User.objects.filter(username=username).values('email')
        try:  # some basic validation of e-mail
            user = auth.sign_in_with_email_and_password(email[0]['email'], password)  # login with e-mail and password
            user_info = auth.get_account_info(user['idToken'])
            if user_info['users'][0]['emailVerified']:
                return super().form_valid(form)
            else:
                messages.error(self.request,
                               'Please verify your email')  # adding the errors in messages list which will be shown in message.html template
                return HttpResponseRedirect(reverse('users:login'))  # Redirecting to form page if there are any errors
        except:
            messages.error(self.request,
                           'Please check your password and e-mail')  # adding the errors in messages list which will be shown in message.html template
            return HttpResponseRedirect(reverse('users:login'))  # Redirecting to form page if there are any errors


class UserLogoutView(LogoutView):  # Initializing template for logout view
    template_name = 'users/login.html'
