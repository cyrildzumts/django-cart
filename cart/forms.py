from django import forms


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantité',
        widget=forms.TextInput(
            attrs={'size': '2', 'value': '1', 'class': 'quantity',
                                'maxlength': '5'}),
        error_messages={'invalid': 'Veuillez saisir une quantité valide.'},
        min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default __init__ to be able to set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # checking for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Les Cookies de votre \
                                            navigateur doivent être activés")
        return self.cleaned_data
