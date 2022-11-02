from django import forms


class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    contact_number_self = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

