from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser
import requests

import os


class SignupForm(UserCreationForm):
    input_class = 'form-control'

    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address',
                             label="Email")

    agree = forms.BooleanField()

    class Meta:
        input_class = 'form-control'

        model = AuthUser

        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):

        site_url = os.environ.get("SITE_URL")
        api_key = os.environ.get("API_KEY")

        # dynamically get form fields
        response = requests.get(site_url + "/api/gender",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        gender = list(zip(list(d["id"] for d in response.json()), list(d["gender"] for d in response.json())))
        self.base_fields["gender"] = forms.ChoiceField(choices=[("", "Select your gender")] + gender,
                                                       label="Gender")

        response = requests.get(site_url + "/api/age",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        ages = list(zip(list(d["id"] for d in response.json()), list(d["age"] for d in response.json())))
        self.base_fields["age"] = forms.ChoiceField(choices=[("", "Select your age")] + ages,
                                                    label="Age")

        response = requests.get(site_url + "/api/country",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        countries = list(zip(list(d["id"] for d in response.json()), list(d["country"] for d in response.json())))
        self.base_fields["country"] = forms.ChoiceField(choices=[("", "Select your country")] + countries,
                                                        label="Country")

        response = requests.get(site_url + "/api/education",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        educations = list(zip(list(d["id"] for d in response.json()), list(d["education"] for d in response.json())))
        self.base_fields["education"] = forms.ChoiceField(choices=[("", "Select your education")] + educations,
                                                          label="Education")

        response = requests.get(site_url + "/api/occupation",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        occupations = list(zip(list(d["id"] for d in response.json()), list(d["occupation"] for d in response.json())))
        self.base_fields["occupation"] = forms.ChoiceField(choices=[("", "Select your occupation")] + occupations,
                                                           label="Occupation")

        input_class = 'form-control'

        for field in self.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["class"] = input_class
            field.widget.attrs["required"] = 'required'
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and AuthUser.objects.filter(email=email).exists():
            raise forms.ValidationError(u'A user with that email already exists.')
        return email


class ProfileForm(forms.Form):

    first_name = forms.CharField(label="Name", max_length=100)
    last_name = forms.CharField(label="Surname", max_length=100)

    def __init__(self, *args, **kwargs):

        site_url = os.environ.get("SITE_URL")
        api_key = os.environ.get("API_KEY")

        # dynamically get form fields
        response = requests.get(site_url + "/api/gender",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        gender = list(zip(list(d["id"] for d in response.json()), list(d["gender"] for d in response.json())))
        self.base_fields["gender"] = forms.ChoiceField(choices=gender,
                                                       label="Gender")

        response = requests.get(site_url + "/api/age",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        ages = list(zip(list(d["id"] for d in response.json()), list(d["age"] for d in response.json())))
        self.base_fields["age"] = forms.ChoiceField(choices=ages,
                                                    label="Age")

        response = requests.get(site_url + "/api/country",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        countries = list(zip(list(d["id"] for d in response.json()), list(d["country"] for d in response.json())))
        self.base_fields["country"] = forms.ChoiceField(choices=countries,
                                                        label="Country")

        response = requests.get(site_url + "/api/education",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        educations = list(zip(list(d["id"] for d in response.json()), list(d["education"] for d in response.json())))
        self.base_fields["education"] = forms.ChoiceField(choices=educations,
                                                          label="Education")

        response = requests.get(site_url + "/api/occupation",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        occupations = list(zip(list(d["id"] for d in response.json()), list(d["occupation"] for d in response.json())))
        self.base_fields["occupation"] = forms.ChoiceField(choices=occupations,
                                                           label="Occupation")

        input_class = 'form-control'

        for field in self.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["class"] = input_class
            field.widget.attrs["required"] = 'required'
        super().__init__(*args, **kwargs)


class BusinessForm(forms.Form):

    def __init__(self, *args, **kwargs):

        site_url = os.environ.get("SITE_URL")
        api_key = os.environ.get("API_KEY")

        # dynamically get form fields
        response = requests.get(site_url + "/api/gender",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        gender = list(zip(list(d["id"] for d in response.json()), list(d["gender"] for d in response.json())))
        self.base_fields["gender"] = forms.ChoiceField(choices=[("", "Select gender")] + gender,
                                                       label="Gender",
                                                       required=False)

        response = requests.get(site_url + "/api/age",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        ages = list(zip(list(d["id"] for d in response.json()), list(d["age"] for d in response.json())))
        self.base_fields["age"] = forms.ChoiceField(choices=[("", "Select age")] + ages,
                                                    label="Age",
                                                    required=False)

        response = requests.get(site_url + "/api/country",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        countries = list(zip(list(d["id"] for d in response.json()), list(d["country"] for d in response.json())))
        self.base_fields["country"] = forms.ChoiceField(choices=[("", "Select country")] + countries,
                                                        label="Country",
                                                        required=False)

        response = requests.get(site_url + "/api/education",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        educations = list(zip(list(d["id"] for d in response.json()), list(d["education"] for d in response.json())))
        self.base_fields["education"] = forms.ChoiceField(choices=[("", "Select education")] + educations,
                                                          label="Education",
                                                          required=False)

        response = requests.get(site_url + "/api/occupation",
                                headers={
                                    "Api-Key": api_key,
                                },
                                )
        occupations = list(zip(list(d["id"] for d in response.json()), list(d["occupation"] for d in response.json())))
        self.base_fields["occupation"] = forms.ChoiceField(choices=[("", "Select occupation")] + occupations,
                                                           label="Occupation",
                                                           required=False)

        input_class = 'form-control'

        for field in self.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["class"] = input_class
        super().__init__(*args, **kwargs)
