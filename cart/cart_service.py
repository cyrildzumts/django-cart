import datetime
from django.db import connection

from cart import models
from demosite import utils
from django.shortcuts import get_object_or_404, Http404

class CartService:


    @staticmethod
    def get_user_cart(request):
        """
            @brief get_user_cart : this is an utility function that
            first checks if the current user is logged in.
            @return a Cart associated to the user who made
            this request.
            An exception is thrown if the user is not logged in.
        """
        if request.user.is_authenticated():
            return CartService.get_cart(request.user)
        else:
            raise Http404("Vous devez être connecter pour \
            pouvoir utiliser le Panier.")

    @staticmethod
    def get_cart(user):
        """
            @brief get_cart
            @param user :  the current user who made the request
            @ return a Cart which belongs to user.
            if the user has no Cart, then a new one is created for this user
        """
        try:
            cart = models.Cart.objects.get(user=user)
        except models.Cart.DoesNotExist:
            cart = models.Cart()
            cart.user = user
            cart.save()
        return cart


    @staticmethod
    def get_subtotal(cart_id):
        total = 0
        result = None
        query = "SELECT  SUM(p.price *content.quantity) as SUM_TOTAL from  cart_items as content \
            LEFT JOIN carts as cart on content.cart_id=cart.id \
            LEFT JOIN Product as p on p.id = content.product_id \
            WHERE content.cart_id=%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [cart_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cartservice : get_subtotal() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            total = result[0]
        return total


    @staticmethod
    def items_count(cart_id):
        count = 0
        result = None
        query = "SELECT SUM(content.quantity) as counter from  cart_items as content \
            WHERE content.cart_id=%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [cart_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cartservice : items_count() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            count = result[0]

        return count

    @staticmethod
    def contains_item(cart_id, product_id):
        flag = False
        result = None
        query = "SELECT  1 from  cart_items as content \
            LEFT JOIN carts as cart on cart.id =content.cart_id \
            WHERE content.cart_id=%s and content.product_id = %s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [cart_id, product_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cartservice : contains_item() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            flag = 1 in result
        return flag
    

    @staticmethod
    def process_request(request):
        postdata = utils.get_postdata(request)
        user_cart = CartService.get_user_cart(request)
        item_id = postdata['item_id']
        quantity = postdata['quantity']
        if postdata['submit'] == 'Supprimer':
            user_cart.remove_from_cart(item_id)
        if postdata['submit'] == 'Actualiser':
            user_cart.update_quantity(item_id=item_id, quantity=int(quantity))
        




def cart_test():
    cart = models.Cart.objects.get(id=32)
    total_1 = cart.subtotal()
    total_2 = CartService.get_subtotal(cart.id)

    counter_1 = cart.items_count()
    counter_2 = CartService.items_count(cart.id)

    flag_1 = cart.contain_item(1)
    flag_2 = CartService.contains_item(cart.id, 1)
    print("total_1 : {0} \n \
           total_2 : {1} \n \
           counter_1 : {2} \n \
           counter_2 : {3}".format(total_1, total_2, counter_1, counter_2))

    print("Flag_1 : {0} \n \
           Flag_2 : {1}".format(flag_1, flag_2))