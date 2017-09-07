import requests
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate

from .forms import SignupForm


def home(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/home.html', context)


def terms(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/terms.html', context)


def about(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/about.html', context)


def delete(request):

    current_user = request.user

    if current_user.is_authenticated:

        # delete platform user
        r = requests.delete("http://localhost:8000/api/user/" + str(current_user))

        # delete gui user
        current_user.delete()

    return redirect('home')


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('first_name')
            surname = form.cleaned_data.get('last_name')
            age = form.cleaned_data.get('age')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            occupation = form.cleaned_data.get('occupation')
            education = form.cleaned_data.get('education')

            r = requests.post("http://localhost:8000/api/user/", data={'username': username,
                                                                       'email': email,
                                                                       'name': name,
                                                                       'surname': surname,
                                                                       'age': age,
                                                                       'gender': gender,
                                                                       'country': country,
                                                                       'occupation': occupation,
                                                                       'education': education})

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'gui/signup.html', {'form': form})
