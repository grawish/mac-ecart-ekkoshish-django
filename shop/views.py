from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
from PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt

MERCHANT_KEY = 'wv!u5hJSoC0W0IXq'
import json


# Create your views here.


def index(request):
    allprods = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, n), nslides])

    params = {'allprods': allprods}
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    # print(request.POST)
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    desc = request.POST.get('desc', '')
    contactx = Contact(name=name, email=email, phone=phone, desc=desc)
    contactx.save()
    return render(request, "shop/contact.html")


def tracker(request):
    if request.method == "POST":
        Oid = request.POST.get("Oid", "")
        email = request.POST.get('email', '')
        try:
            orders = Order.objects.filter(odr_id=Oid, email=email)
            if len(orders) > 0:
                update = OrderUpdate.objects.filter(odr_id=Oid)
                updates = []
                response = ""
                for items in update:
                    updates.append({'text': items.update_desc, 'time': items.timestamp})
                    response = json.dumps([updates, orders[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse("{}")
    return render(request, 'shop/tracker.html')


def prod(request, idx):
    # fetch products by id
    product = Product.objects.filter(id=idx)
    params = {'product': product[0]}
    return render(request, "shop/prodView.html", params)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprods.append([prod, range(1, n), nslides])

    params = {'allprods': allprods}
    return render(request, "shop/index.html", params)


def checkout(request):
    done = 'false'
    oid = ""
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('Amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipc = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address1 + " " + address2, city=city,
                      state=state, zip=zipc, phone=phone, amount=amount)
        order.save()
        done = "true"
        oid = str(order.odr_id)
        # request paytm to transfer the amount in account after payment by user
        params_dict = {
            'MID': 'AVDJtl54275283159763',
            'ORDER_ID': str(order.odr_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://localhost:8000/shop/handlerequest/',
        }
        params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, MERCHANT_KEY)
        return render(request, "shop/paytm.html", {'param_dict': params_dict})

    return render(request, "shop/checkout.html", {'done': done, 'id': oid})


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print(response_dict)
            update = OrderUpdate(odr_id=response_dict['ORDERID'], update_desc="The order has been placed")
            update.save()
            Order.objects.filter(odr_id=response_dict['ORDERID']).update(paymentstatus=True,
                                                                         paymentid=response_dict['TXNID'],
                                                                         bankid=response_dict['BANKTXNID'])
    else:
        print("Order was not successful because " + response_dict['RESPMSG'])
        update = OrderUpdate(odr_id=response_dict['ORDERID'], update_desc=response_dict['RESPMSG'])
        update.save()
        Order.objects.filter(odr_id=response_dict['ORDERID']).update(paymentstatus=False)
    return render(request, 'shop/paymentstatus.html', {"response": response_dict})


def cart(request):
    return render(request, 'shop/cart.html')
