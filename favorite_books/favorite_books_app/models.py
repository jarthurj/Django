from django.db import models
from django.contrib import messages
import re
import datetime
from datetime import date,timedelta

class UserManager(models.Manager):
	def register_validation(self, postData):
		birthday = date.fromisoformat(postData['birthday'])
		# delta_thirteen = date.today() - timedelta(days=4745)
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		email_exist = User.objects.filter(email=postData['email'])
		if len(email_exist) != 0:
			if postData['email'] == email_exist[0].email:
				errors['user_exist'] = "User already exists"
		if len(postData['first_name']) < 3:
			errors['first_name'] = "First name must be more than 2 characters"
		if len(postData['last_name']) < 3:
			errors['last_name'] = "Last name must be more than 2 characters"
		if postData['password'] != postData['confirm']:
			errors['password'] = "Passwords do not match!"
		# if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
		# 	errors['email'] = "Invalid email address!"
		if len(postData['password']) < 8:
			errors['passlen'] = "Password must be longer than 8 characters"


		if not UserManager.age_verification(birthday):
			errors['birthday'] = "You must be at least 13 years old to register"


		return errors
	def age_verification(birthday):
		today = date.today()
		year_diff = today.year - birthday.year
		if year_diff > 13:
			return True
		elif year_diff < 13:
			return False
		else:
			month_diff = today.month - birthday.month
			if month_diff < 0:
				return False
			else:
				day_diff = today.day - birthday.day 
				if day_diff < 0:
					return False
				else:
					return True



class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	birthday = models.DateField(auto_now=False, auto_now_add=False)
	hashed_pw = models.CharField(max_length=255)
	objects = UserManager()
	def __str__(self):
		return f"{self.first_name} {self.last_name} {self.email} {self.birthday} {self.hashed_pw}"

class BookManager(models.Manager):
	def validate_book(self, postData):

		errors = {}

		if postData['title'] == "":
			errors['title'] = "Book must have title"
		if len(postData['description']) < 5:
			errors['description'] = "description must be longer than 5 characters"


		return errors

class Book(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
	user_favorite = models.ManyToManyField(User, related_name="favorite_books")
	objects = BookManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return f"{self.title}"
