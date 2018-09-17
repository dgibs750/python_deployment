from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def reg_validations(self, postData):
        errors = {}
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be no less than 2 characters and contain only letters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be no less than 2 characters and contain only letters"
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 1:
            errors["email"] = "Email cannot be blank and must be valid"
        user = User.objects.filter(email=postData['email'])
        if user:
            errors['exists'] = 'User already exists'
        else:
            if len(postData['password']) < 8:
                errors['password'] = 'Password should be more than 8 characters long.'
            if postData['password'] == postData['confirm_password']:
                print('passwords match')
            else:
                errors['match'] = 'Passwords need to match'
        if not errors:
            psswrd = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=psswrd)
            errors['uid'] = user.id
        return errors

    def login_validations(self, postData):
        errors = {}
        user_check = User.objects.filter(email=postData['email'])
        if user_check:
            user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Email or Password doesn't match"
            else:
                errors['uid'] = user.id
        else:
            errors['password'] = "Email or Password doesn't match"
        return errors

    def update_validations(self, postData):
        errors = {}
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be no less than 2 characters and contain only letters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be no less than 2 characters and contain only letters"
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 1:
            errors["email"] = "Email cannot be blank and must be valid"
        user = User.objects.filter(email=postData['email'])
        if postData['email'] != User.objects.get(id=postData['uid']).email:
            if user:
                errors['exists'] = 'Email is already in use'
        if not errors:
            errors['pass'] = 1
        return errors


class QuoteManager(models.Manager):
    def quote_validations(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = 'Authors name should be more than 3 characters'
        if len(postData['quote']) < 10:
            errors['quote'] = 'Quote should be at least 10 characters'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return f'User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}'


class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name='quotes')
    liked_by = models.ManyToManyField(User, related_name='likes')

    objects = QuoteManager()

    def __repr__(self):
        return f'Quote(id={self.id}, Author={self.author}, Quote={self.quote}, Uploaded_by={self.uploaded_by}'