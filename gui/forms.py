from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser
import requests


class SignupForm(UserCreationForm):
    input_class = 'form-control'

    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address',
                             label="Email")

    class Meta:
        input_class = 'form-control'

        model = AuthUser

        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):

        # dynamically get form fields
        response = requests.get("http://localhost:8000/api/age")
        ages = list(d["age"] for d in response.json())
        self.base_fields["age"] = forms.ChoiceField(choices=[("", "Select your age")] + list(zip(ages, ages)),
                                                    label="Age")

        response = requests.get("http://localhost:8000/api/country")
        countries = list(d["country"] for d in response.json())
        self.base_fields["country"] = forms.ChoiceField(choices=[("", "Select your country")] + list(zip(countries, countries)),
                                                        label="Country")

        response = requests.get("http://localhost:8000/api/education")
        educations = list(d["education"] for d in response.json())
        self.base_fields["education"] = forms.ChoiceField(choices=[("", "Select your education")] + list(zip(educations, educations)),
                                                          label="Education")

        response = requests.get("http://localhost:8000/api/occupation")
        occupations = list(d["occupation"] for d in response.json())
        self.base_fields["occupation"] = forms.ChoiceField(choices=[("", "Select your occupation")] + list(zip(occupations, occupations)),
                                                           label="Occupation")

        input_class = 'form-control'
        
        for field in self.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["class"] = input_class
            field.widget.attrs["required"] = 'required'
        super(UserCreationForm, self).__init__(*args, **kwargs)
