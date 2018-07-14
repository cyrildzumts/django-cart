from django.contrib.auth.models import User
from .models import Cart


def test_cart():
    user = User.objects.get(username='cyrildz')
    ucart = Cart.objects.get(user=user)
    ci_first = ucart.cartitem_set.first()
    pk = ci_first.product.pk
    print("Cart contains item with id",
          ci_first.product.pk, ":",  ucart.contain_item(pk))
    print("Cart contains item with id 0 ? :", ucart.contain_item(0))
    print("Cart contains item with id 45 ? :", ucart.contain_item(45))
    print("Cart contains item with id 3 ? :", ucart.contain_item(-3))
    print("Cart Is Empty ?:", ucart.is_empty())
    print("Cart items count :", ucart.items_count())
