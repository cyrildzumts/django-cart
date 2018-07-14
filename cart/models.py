from django.db import models
import datetime
from catalog.models import Product, ProductVariant, VariantOption, Color, Size
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.conf import settings
# from django.contrib.sessions.models import Session
# from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from cart.cart_exceptions import QuantityError
from django.core.exceptions import ObjectDoesNotExist

from cart.cart_service import CartService
# Create your models here.

"""
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session)


def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
    )

user_logged_in.connect(user_logged_in_handler)


def delete_user_session(user):
    user_sessions = UserSession.objects.filter(user=user)
    for user_session in user_sessions:
        user_session.session.delete()

"""


class Cart(models.Model):
    """
    Every User has a Cart.
    When checking out a Cart, an Order can be created from a  Cart.
    """
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']

    def __str__(self):
        return "Cart id : %d\nUser :%s" % (self.id, self.user)

    def add_to_cart(self, product, quantity=1):
        """
        Add a new product into the Shopping Cart.
        If the product is already in the cart then
        update the quantity.
        If not then create a new CartItem and set
        appropriate value for its variable and save.
        This method does nothing when 'quantity' <  1
        """
        added = False
        if quantity >= 0:
            if CartService.contains_item(self.id, product.id):
                print ("Product Already in Cart")
                # ci = CartItem.objects.get(product=product)
                # ci = CartItem.objects.get(cart=self, product=product)
                ci = self.cartitem_set.get(product=product)
                added = self.update_quantity(ci.id, quantity)

            # check if this product is already in the cart.
            # if yes, then check if 'quantity' is not greater than
            # that we have in stock.
            # if it is lower then update the quantity in stock

            else:
                # create and save a new cart item
                if (quantity <= (product.quantity - product.sell_quantity)):
                    item = CartItem()
                    item.set_product(product)
                    # this might throw an exception
                    item.set_quantity(quantity)
                    item.set_cart(self)
                    item.save()
                    added = True
        return added

    def contain_item(self, item_id):
        """
        Deprecated : this method is slow on query.
        Use the CartService.contains_items() from 
        cart.cart_service instead
        """
        """
        flag = False
        try:
            start_time = datetime.datetime.now()
            prod = Product.objects.get(pk=int(item_id))
            item = self.cartitem_set.get(product=prod)
            if item is not None:
                flag = True
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cart : contain_item() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        except ObjectDoesNotExist as e:
            flag = False
        """
        return CartService.contains_item(self.id, item_id)

    def get_item(self, item_id):
        """
        Return a CartItem object when found
        """
        try:
            item = CartItem.objects.get(pk=item_id, cart=self)
        except ObjectDoesNotExist:
            item = None
        return item

    def update_cart(self, item_id, quantity):
        """
        item_id : ID of the Product to be updated
        quantity:  new quantity of the item .
        precondition : quantity >= 0;
        update_cart() updates the quantity value of a CartItem.
        If quantity == 0 then that item will be removed from the cart.
        if quantity < 0 this method returns false.
        On success this method returns True.

        Update :11.03.2018 : this method returns an object which
        contains more infos on the result.
        """
        response = {}
        if(quantity >= 0):
            if(CartService.contains_item(self.id, item_id)):
                prod = Product.objects.get(pk=int(item_id))
                item = self.cartitem_set.get(product=prod)
                # item = self.get_item(item_id)
                # item_quantity = item.get_quantity()
                if quantity > 0:
                    in_stock = prod.quantity - prod.sell_quantity
                    if (quantity <= in_stock):
                        item.set_quantity(quantity)
                        item.save()
                        response['updated'] = True
                        response['quantity'] = quantity
                    else:
                        response['updated'] = False
                        response['quantity_error'] = True
                        response['quantity'] = item.quantity

                else:
                        response['updated'] = self.remove_from_cart(item.id)
                        response['quantity'] = 0
        return response


    def update_quantity(self, item_id, quantity):
            """
            Update the CartItem quantity to the value
            of quantity.
            item_id : CartItem id.
            If quantity = 0, the corresponding CartItem will
            be deleted.
            This method return True if the quantity could be updated.
            return False if not.
            """
            flag = False
            item = self.get_item(item_id)
            if item:
                # item_quantity = item.get_quantity()
                if quantity > 0:
                    in_use = item.get_quantity()
                    desired_qty = in_use + quantity
                    in_stock = item.get_product().quantity - item.get_product().sell_quantity 
                    if (in_stock >= desired_qty):
                        item.set_quantity(desired_qty)
                        item.save()
                        print("Cart item qty augmented")
                        flag = True
                    else:
                        print("Cart item qty not available")
                else:
                    if quantity == 0:
                        flag = self.remove_from_cart(item_id)
            return flag

    def remove_from_cart(self, item_id):
        """
        Delete the CartItem corresponding to item_id.
        """
        flag = False
        item = self.get_item(item_id)
        if item:
            item.delete()
            flag = True
        return flag

    def subtotal(self):
        """
        Return the subtotal amount for the
        items available in the Cart.
        Deprecated : use CartService.get_subtotal()
        from cart.cart_service instead
        """
        """
        cart_total = 0
        start_time = datetime.datetime.now()
        items = self.get_items()
        for item in items:
            cart_total += item.total_price()

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Cart : subtotal() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        """
        return CartService.get_subtotal(self.id)

    def get_items(self):
        """
        Return all the items present in the Cart.
        """
        return self.cartitem_set.all()

    def items_count(self):
        """
        Return the number of items present in the Cart.
        Deprecated : use CartService.items_count()
        from cart.cart_service instead
        """
        """
        count = 0
        start_time = datetime.datetime.now()
        items = self.get_items()
        for item in items:
            count += item.quantity

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Cart : items_count() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        """
        return CartService.items_count(self.id)

    def is_empty(self):
        return self.items_count() == 0

    def get_user(self):
        return self.user

    def get_id(self):
        return self.id


class CartItem(models.Model):
    """
    CartItem represents the an Item present in a Cart.
    A CartItem can be parts of many Carts.
    CartItem is generic representation of the Product class,
    so much of all message send to this instance is delegated to
    the associated product member.
    """
    cart = models.ForeignKey(Cart, unique=False, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('catalog.Product', unique=False)
    variantOption = models.ForeignKey(VariantOption, unique=False, null=True,blank=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def __str__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def set_quantity(self, quantity):
        flag = False
        if quantity <= self.variantOption.quantity:
            self.quantity = quantity
            flag = True
        """
        else:
            raise QuantityError(available=self.product.quantity,
                                value=quantity)
        """
        return flag

    def get_quantity(self):
        return self.quantity

    
    def set_variant_option(self, variant):
        self.variantOption = variant

    def set_product(self, product):
        self.product = product

    def get_product(self):
        return self.product

    def set_cart(self, cart):
        self.cart = cart

    def get_cart(self):
        return self.cart

    def total(self):
        return self.product.price * self.quantity

    def name(self):
        return self.product.name
    
    def image(self):
        return self.product.image

    def image_url(self):
        return self.product.image.url
    
    def price(self):
        return self.variantOption.price

    def total_price(self):
        return self.price() * self.quantity

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def change_quantity(self, quantity):
        if quantity <= self.product.quantity:
            self.quantity = quantity
            self.save()
        else:
            raise QuantityError(available=self.product.quantity,
                                value=quantity)


class LineItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(
                type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(LineItemManager, self).get(*args, **kwargs)


class LineItem(models.Model):
    unit_price = models.IntegerField()
    quantity = models.PositiveIntegerField()

    # defining product as a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LineItemManager()

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ['-created_at']

    def __str__(self):
        return "%d pieces de %s" % (
            self.quantity, self.product.__class__.__name__)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    # product definition
    @property
    def product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    @product.setter
    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk
