from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..algorithms import update_prof


@api_view(['POST'])
def update_profile(request, username, *args, **kwargs):

    message = update_prof(request, username)

    return Response({"message": message})
