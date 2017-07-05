from django.http import HttpResponse
from django.template import loader


def home(request, *args, **kwargs):

    template = loader.get_template('gui/home.html')
    context = {}

    return HttpResponse(template.render(context, request))
