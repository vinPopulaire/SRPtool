from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from django.contrib.auth import login, authenticate

from .forms import SignupForm


def home(request, *args, **kwargs):

    template = loader.get_template('gui/home.html')
    context = {}

    return HttpResponse(template.render(context, request))


def terms(request, *args, **kwargs):

    template = loader.get_template('gui/terms.html')
    context = {}

    return HttpResponse(template.render(context, request))


def about(request, *args, **kwargs):

    template = loader.get_template('gui/about.html')
    context = {}

    return HttpResponse(template.render(context, request))


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'gui/signup.html', {'form': form})
