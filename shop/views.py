from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
#from django.views.decorators.csrf import csrf_exempt
#from Paytm import Checksum
#MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';

# Create your views here.
def index(request):
    #products = Product.objects.all()
    #print(products)
   # n = len(products)
    #nslides = n//4 + ceil((n/4)-(n//4))
    #params = {'no_of_slides': nslides, 'range': range(1, nslides), 'product': products}
    #allprods = [[products, range(1, nslides), nslides], [products, range(1, nslides), nslides]]

    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod, range(1, nslides), nslides])

    params = {'allprods':allprods}
    return render(request,'shop/index.html', params)

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allprods.append([prod, range(1, nslides), nslides])

    params = {'allprods': allprods}
    if len(allprods) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevent search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timesramp})
                    response = json.dumps({"status":"success", "updates":updates, "itemJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')




def pruductview(request, myid):
    #fetch the product using id
    products = Product.objects.filter(id=myid)
    print(products)
    return render(request,'shop/productview.html', {'product':products[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        amount = request.POST.get('amount', '')
        address = request.POST.get('address1', '')+" "+request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        payment = request.POST.get('payment', '')
        order = Order(items_json=items_json, name=name, payment=(payment), email=email, amount=amount, address=address, city=city,
                      state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="tomorrow your order will be shipped")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        '''        
        #request paytm to tranfer the amount to your account after payment by user
        
        param_dict = {
            'MID': 'WorldP64425807474247', # paytm merchant id
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',

            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'shop/paytm.html', {'param_dict': param_dict})
        '''
    return render(request, 'shop/checkout.html')

'''
@csrf_exempt
def handlerequest(request):
    return HttpResponse("done")
'''
