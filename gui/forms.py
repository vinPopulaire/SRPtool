from django import forms


class SignupForm(forms.Form):
    # CSS styles should not be inline. i've moved your style contents under a 'form-control' class
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'text',
                                                                             'placeholder': 'Enter your username',
                                                                             'id': 'name',
                                                                             'name': 'name',
                                                                             'class': 'form-control'}))
    email = forms.EmailField(label="Email address", widget=forms.TextInput(attrs={'type': 'text',
                                                                                  'placeholder': 'Your E-mail',
                                                                                  'id': 'email',
                                                                                  'name': 'email',
                                                                                  'class': 'form-control'}))
    pass1 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'password',
                                                                         'placeholder': 'Password',
                                                                         'id': 'pass1',
                                                                         'name': 'pass1',
                                                                         'class': 'form-control'}))
    pass2 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'password',
                                                                         'placeholder': 'Confirm Password',
                                                                         'id': 'pass2',
                                                                         'name': 'pass2',
                                                                         'class': 'form-control'}))
