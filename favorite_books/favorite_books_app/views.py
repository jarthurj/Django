from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt
import datetime

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
		return redirect('/welcome')
	
def process_login(request):
	user = User.objects.filter(email = request.POST['email'])
	if user:
		logged_user = user[0]
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.hashed_pw.encode()):
			request.session['userid'] = logged_user.id
			request.session['name'] = logged_user.first_name
			return redirect('/welcome')
		else:
			messages.error(request, "Passord Incorrect")
			return redirect('/')
	else:
		messages.error(request, "Email not found")
		return redirect("/")

def welcome(request):
	if 'userid' in request.session:
		user = User.objects.get(id=request.session['userid'])
		favorites = user.favorite_books.all()
		context = {
			'books' : Book.objects.all(),
			'favorites': favorites,
		}
		return render(request,'welcome.html', context)
	else:
		return redirect('/')


def add_book(request):
	errors = Book.objects.validate_book(request.POST)
	user=User.objects.get(id=request.session['userid'])
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/welcome')
	else:
		new_book = Book.objects.create(title=request.POST['title'],description=request.POST['description'], user=user)
		new_book.user_favorite.add(user)
		return redirect('/welcome')

def add_fav(request, book_id):
	user=User.objects.get(id=request.session['userid'])
	new_fav_book = Book.objects.get(id=book_id)
	new_fav_book.user_favorite.add(user)
	return redirect('/welcome')

def log_off(request):
	request.session.flush()
	return redirect('/')

def edit_fav(request, book_id):
	book = Book.objects.get(id=book_id)
	request.session['edit_book_id'] = book_id
	context = {
		'book':book
	}
	return render(request, 'book.html', context)
def view_book(request, book_id):
	book = Book.objects.get(id=book_id)
	user = User.objects.get(id=request.session['userid'])
	favorites = user.favorite_books.all()
	context = {
		'book':book,
		'favorites': favorites,
	}
	return render(request, 'viewbook.html', context)
def unfav(request, book_id):
	user = User.objects.get(id= request.session['userid'])
	user.favorite_books.remove(Book.objects.get(id=book_id))
	user.save()
	return redirect('/welcome')

def delete_book(request, book_id):
	book_to_delete = Book.objects.get(id=book_id)
	book_to_delete.delete()
	return redirect('/welcome')

def process_edit(request):
	errors = Book.objects.validate_book(request.POST)
	user=User.objects.get(id=request.session['userid'])
	book_edit_id = request.session['edit_book_id']
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect(f"/book/fav/{book_edit_id}")
	else:
		title = request.POST['title']
		description = request.POST['description']
		book_id = request.POST['book_id']
		book_to_update = Book.objects.get(id=book_id)
		if title != book_to_update.title:
			book_to_update.title = title
			book_to_update.save()
		if description != book_to_update.description:
			book_to_update.description = description
			book_to_update.save()
		return redirect('/welcome')

def favorites(request, user_id):
	if request.session['userid'] != user_id:
		request.session.flush()
		return redirect('/')
	else:
		user = User.objects.get(id=user_id)
		favorites = user.favorite_books.all()
		context = {
			'favorites': favorites,
			'name':user.first_name
		}
		return render(request, 'favbooks.html', context)