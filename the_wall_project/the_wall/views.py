from django.shortcuts import render, redirect
from .models import User, UserManager, Message, Comment
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
		new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email
			,birthday=birthday, hashed_pw=pw_hash)
		request.session['userid'] = new_user.id
		request.session['first_name'] = first_name
		return redirect('/wall')
	
def process_login(request):
	user = User.objects.filter(email = request.POST['email'])
	if user:
		logged_user = user[0]
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.hashed_pw.encode()):
			request.session['userid'] = logged_user.id
			request.session['name'] = logged_user.first_name
			return redirect('/wall')
		else:
			messages.error(request, "Passord Incorrect")
			return redirect('/')
	else:
		messages.error(request, "Email not found")
		return redirect("/")

def wall(request):
	context = {
		'wall_messages': Message.objects.all()
	}
	return render(request,'wall.html', context)

def log_off(request):
	request.session.flush()
	return redirect('/')

def post_message(request):
	user = User.objects.get(id=request.session['userid'])
	Message.objects.create(message=request.POST['new_message'], user=user)
	return redirect('/wall')

def post_comment(request, message_id):
	user = User.objects.get(id=request.session['userid'])
	message = Message.objects.get(id=message_id)
	Comment.objects.create(comment=request.POST['new_comment'], user=user, message=message)
	return redirect('/wall')




