from django.db import models
from django.contrib import messages
import re

class UserManager(models.Manager):
	def register_validation(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['first_name']) < 3:
			errors['first_name'] = "First name must be more than 2 characters"
		if len(postData['last_name']) < 3:
			errors['last_name'] = "Last name must be more than 2 characters"
		if postData['password'] != postData['confirm']:
			errors['password'] = "Passwords do not match!"
		if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
			errors['email'] = ("Invalid email address!")
		if len(postData['password']) < 8:
			errors['passlen'] = "Password must be longer than 8 characters"
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	birthday = models.DateField(auto_now=False, auto_now_add=False)
	hashed_pw = models.CharField(max_length=255)
	objects = UserManager()
	def __str__(self):
		return f"{self.first_name} {self.last_name} {self.email} {self.birthday} {self.hashed_pw}"


