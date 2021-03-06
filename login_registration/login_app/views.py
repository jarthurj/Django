from django.shortcuts import render, redirect
from .models import User, UserManager
from django.contrib import messages

import bcrypt
def index(request):
	return render(request, 'index.html')


def process_registration(request):
	errors = User.objects.register_validation(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"]
		birthday = request.POST["birthday"]
		password = request.POST['password']
		pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		User.objects.create(first_name=first_name, last_name=last_name, email=email
			,birthday=birthday, hashed_pw=pw_hash)
		request.session['first_name'] = first_name
		return redirect('/success')

def process_login(request):
	user = User.objects.filter(email = request.POST['email'])
	if user:
		logged_user = user[0]
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.hashed_pw.encode()):
			request.session['userid'] = logged_user.id
			return redirect('/success')
		else:
			messages.error(request, "Passord Incorrect")
			return redirect('/')
	else:
		messages.error(request, "Email not found")
		return redirect("/")


def success(request):
	if 'userid' in request.session:
		user = User.objects.filter(id = request.session['userid'])
		if user:
			context = {
				'first_name':user[0].first_name
			}
			return render(request, 'success.html')
	return redirect('/')

def log_out(request):
	request.session.flush()
	return redirect('/')



