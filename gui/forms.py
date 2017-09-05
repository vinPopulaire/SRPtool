from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser


class SignupForm(UserCreationForm):
    input_class = 'form-control'

    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Your Email',
                                                           'class': input_class}))

    class Meta:
        input_class = 'form-control'

        model = AuthUser

        fields = ('username', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        input_class = 'form-control'
        
        for field in self.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["class"] = input_class
        super(UserCreationForm, self).__init__(*args, **kwargs)
