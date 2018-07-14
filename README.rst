==========
Cart
==========

Cart is a Django app to provide a shopping Cart facility to a
Django Website.
The Cart use Django Content Type to provide generic Model Type
support so that you don't have to think about the Models the 
Site is using.

For a detailed documentation please have a look in the "docs" directory.

Quick start :
-------------

1. Add "cart" to your INSTALLED_APPS setting like this :
	INSTALLED_APPS = [
		...
		'cart',
	
	]

2. Include the cart URLConf in your project urls.py like this :
	url(r'^cart/', include('cart.urls')),
	

3. Run 'python manage.py migrate' to create the cart models.

4. Use CartItemForm to add Cart Item into the cart

5. Visit localhost:8000/cart to see the cart.
