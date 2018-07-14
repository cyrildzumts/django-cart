from django.test import TestCase
from .models import Cart, CartItem
from catalog.models import Product


# LG G3 Information
# pk : 3
# quantity : 1
# activ : yes

# Ballerine Loafer
# pk : 1
# quantity : 6
# activ : yes

class CartTestCase(TestCase):
    # fixtures=['catalog']

    def setUp(self):
        self.noprod = Product()
        self.lg3 = Product()
        self.loafer = Product()

        self.noprod.activ = False
        self.noprod.quantity = 10
        self.noprod.pk= 19
        self.noprod.name = 'No product'

        # LG3 Product
        self.lg3.pk = 3
        self.lg3.quantity = 1
        self.lg3.name = 'LG 3'

        # Loafer Product
        self.loafer.pk = 1
        self.loafer.quantity = 6
        self.loafer.name = 'Loafer'

    def test_add_to_cart(self):
        """
        It should only be possible to add item
        into the cart only if the product and quantity
        are corrects.
        """
        pass

# Create your tests here.
