from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import time
#just import everything you need ok

#validation stuff
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
    def register(self, **kwargs):
        print "** now using user manager **"
        print "** registration in process! **"
        status = {}
        messages = []
        f_name = kwargs['first_name'][0]
        l_name = kwargs['last_name'][0]
        email = kwargs['email'][0]
        password = kwargs['password'][0]
        confirm_password = kwargs['confirm_password'][0]
        birthday = kwargs['birthday'][0]
        print birthday
        #checking first name
        if len(f_name) <= 1:
            messages.append('First name has to be at least 2 characters.')
        elif not NAME_REGEX.match(f_name):
            messages.append('First name can only contain letters.')
        #checking last name
        if len(l_name) <= 1:
            messages.append('Last name has to be at least 2 characters.')
        elif not NAME_REGEX.match(l_name):
            messages.append('Last name can only contain letters.')
        #checking email
        if len(email) < 1:
            messages.append('E-mail is required.')
        elif not EMAIL_REGEX.match(email):
            messages.append('Invalid e-mail format.')
        elif len(User.userManager.filter(email=email)) > 0:
            messages.append('User already exists.')
        #checking password
        if len(password) < 8:
            messages.append('Password should be at least 8 characters.')
        elif password != confirm_password:
            messages.append('Password fields do not match.')
        #checking birthday
        if not re.search(r'^[0-9][0-9][0-9][0-9][\-][0-9][0-9][\-][0-9][0-9]', birthday):
            messages.append('Invalid birthday format. Should be YYYY-MM-DD format.')
        elif birthday > time.strftime("%Y-%m-%d"):
            messages.append('Invalid birthday! Need to be from the past.')

        if not messages:
            valid = True
            messages.append('Thank you for registering! Please sign in.')
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.userManager.create(first_name = f_name, last_name = l_name, email = email, password = pw_hash, birthday = birthday)
        else:
            valid = False

        status.update({'valid': valid, 'messages': messages})
        return status

    def login(self, **kwargs):
        print "** Using user manager **"
        print "** Checking login **"
        status = {}
        messages = []
        email = kwargs['email'][0]
        password = kwargs['password'][0]
        print email, password

        if len(email) < 1 or len(password) < 1:
            messages.append("Login fields cannot be blank.")
        else:
            userinfo = User.userManager.filter(email=email)
            if not userinfo:
                messages.append("Unable to find user. Please register.")
            elif not bcrypt.checkpw(password.encode(), userinfo[0].password.encode()):
                messages.append("Incorrect password.")

        if not messages:
            valid = True
            status.update({'user_id': userinfo[0].id})
        else:
            valid = False
            status.update({'messages': messages})
        status.update({'valid': valid})
        return status

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    birthday = models.DateField(auto_now = False, auto_now_add = False)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # def __str__(self):
    # return self.first_name + " " + self.last_name
    userManager = UserManager()
