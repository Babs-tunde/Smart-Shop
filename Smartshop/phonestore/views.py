from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Phone, Invoice
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    phones = Phone.objects.all()
    return render(request, 'home.html',{'phones': phones})

@login_required
def phone_list(request):
    phones = Phone.objects.all()
    return render(request, 'phone_list.html', {'phones': phones})

@login_required
def create_invoice(request):
    if request.method == 'POST':
        phone = Phone.objects.get(id=request.POST['phone'])
        phone.stock -= int(request.POST['quantity'])
        phone.save()

        invoice = Invoice(customer_name=request.POST['customer_name'],
                          customer_address=request.POST['customer_address'],
                          date=request.POST['date'],
                          phone=phone,
                          quantity=request.POST['quantity'])
        invoice.save()
        return redirect('invoice_list')
    else:
        phones = Phone.objects.all()
        return render(request, 'create_invoice.html', {'phones': phones})


# def create_invoice(request):
#     if request.method == 'POST':
#         customer_name = request.POST['customer_name']
#         customer_address = request.POST['customer_address']
#         date = request.POST['date']
#         total_amount = 0
#         for i in range(len(request.POST.getlist('phone'))):
#             phone = Phone.objects.get(pk=request.POST.getlist('phone')[i])
#             quantity = request.POST.getlist('quantity')[i]
#             total_amount += phone.price * int(quantity)
#             invoice = Invoice.objects.create(customer_name=customer_name, customer_address=customer_address, date=date, phone=phone, quantity=quantity)
#         invoice.total_amount = total_amount
#         invoice.save()
#         return redirect('invoice_list')
#     else:
#         phones = Phone.objects.all()    
#         return render(request, 'create_invoice.html', {'phones': phones})


# def invoice_list(request):
#     invoices = Invoice.objects.all()
#     return render(request, 'invoice_list.html', {'invoices': invoices})
@login_required
def invoice_list(request):
    if request.method == 'POST':
        date = request.POST["date"]
        invoices = Invoice.objects.filter(date=date)
    else:
        invoices = Invoice.objects.all()
    for invoice in invoices:
        invoice.price = invoice.quantity * invoice.phone.price

    paginator = Paginator(invoices, 10)  
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger: 
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    return render(request, 'invoice_list.html', {'invoices': invoices})


def stock_data(request):
    phones = Phone.objects.values('name', 'stock')
    return JsonResponse(list(phones), safe=False)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'There was an error with your submission.please check the form for errors and try again.'
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('login'))
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})