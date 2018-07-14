import json
from django.shortcuts import render
from catalog.models import Product
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.urls import reverse, resolve
from cart.cart_service import CartService
# from cart.models import Cart, CartItem
from demosite import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from order import checkout

# Create your views here.


@csrf_protect
@login_required
def show_cart(request):
    template_name = "cart/cart_flat.html"
    user_cart = CartService.get_user_cart(request)
    # checkout_url = checkout.get_checkout_url(request)
    match = resolve('/order/checkout/')

    if request.method == "POST":
        postdata = request.POST.copy()
        item_id = postdata['item_id']
        quantity = postdata['quantity']
        if postdata['submit'] == 'Supprimer':
            user_cart.remove_from_cart(item_id)
        elif postdata['submit'] == 'Actualiser':
            user_cart.update_quantity(item_id=item_id, quantity=int(quantity))

    cart_items = user_cart.get_items()
    page_title = 'Panier' + " - " + settings.SITE_NAME
    cart_subtotal = CartService.get_subtotal(user_cart.id)
    cart_item_count = CartService.items_count(user_cart.id)

    context = {'cart_items': cart_items,
               'page_title': page_title,
               'cart_item_count': cart_item_count,
               'cart_subtotal': cart_subtotal,
               'checkout_url': match.url_name,
            }

    return render(request=request,
                  template_name=template_name,
                  context=context)
# Create your views here.


# ajax-add To cart view
@csrf_exempt
def ajax_add_to_cart(request):

    response = {}
    response['state'] = False
    added = False
    request_is_valid = len(request.POST) > 0
    if request_is_valid:
        postdata = request.POST.copy()
        product_id = postdata['product_id']
        quantity = postdata['quantity']
        if product_id:
            user_cart = CartService.get_user_cart(request)
            p = Product.objects.get(pk=product_id)
            added = user_cart.add_to_cart(product=p, quantity=int(quantity))
            if added is True:
                response['state'] = True
                response['count'] = CartService.items_count(user_cart.id)
                response['total'] = CartService.get_subtotal(user_cart.id)
            else:
                return HttpResponseBadRequest()
    return HttpResponse(json.dumps(response),
                        content_type="application/json")


# ajax cart update view.
@csrf_exempt
def ajax_cart_update(request):
    """
    This method is called from JQuery.  it updates the Cart
    When 
    """
    response = HttpResponseBadRequest()
    result = {}
    request_is_valid = len(request.POST) > 0
    if request_is_valid:
        
        postdata = request.POST.copy()
        product_id = int(postdata['product_id'])
        quantity = int(postdata['quantity'])
        if product_id is not None and quantity is not None:
            user_cart = CartService.get_user_cart(request)
            result = user_cart.update_cart(item_id=product_id, quantity=quantity)
            result['count'] = CartService.items_count(user_cart.id)
            result['total'] = CartService.get_subtotal(user_cart.id)
            response = result
                
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(response),
                        content_type="application/json")
