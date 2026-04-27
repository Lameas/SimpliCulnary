from django import forms


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nom complet",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Telephone",
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Adresse",
    )
    city = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Ville",
    )
