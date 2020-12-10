from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    prod = Product.objects.get(id = request.POST["price"])
    price_from_form = float=(prod.price)
    total_charge = quantity_from_form * price_from_form
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    print("Charging credit card...")
    all_quantity = 0
    all_price = 0
    for order in Order.objects.all():
        all_quantity += order.quantity_ordered
        all_price += order.total_price
    if price_from_form % 1 == 0:
        price_from_form = f"{price_from_form}0"
    request.session["price"] = str(price_from_form)
    request.session["all_q"] = str(all_quantity)
    request.session["all_p"] = str(all_price)
    return redirect("/display_checkout")

def display_checkout(request):
    context = {
        "price" : request.session["price"],
        "all_q" : request.session["all_q"],
        "all_p" : request.session["all_p"]
    }
    return render(request, "store/checkout.html", context)