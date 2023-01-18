from django.shortcuts import render, redirect
from .models import Phone, Invoice
from django.http import JsonResponse

# Create your views here.

def home(request):
    phones = Phone.objects.all()
    return render(request, 'home.html',{'phones': phones})

def phone_list(request):
    phones = Phone.objects.all()
    return render(request, 'phone_list.html', {'phones': phones})

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

def invoice_list(request):
    if request.method == 'POST':
        date = request.POST["date"]
        invoices = Invoice.objects.filter(date=date)
    else:
        invoices = Invoice.objects.all()
    for invoice in invoices:
        invoice.price = invoice.quantity * invoice.phone.price
    return render(request, 'invoice_list.html', {'invoices': invoices})


def stock_data(request):
    phones = Phone.objects.values('name', 'stock')
    return JsonResponse(list(phones), safe=False)
