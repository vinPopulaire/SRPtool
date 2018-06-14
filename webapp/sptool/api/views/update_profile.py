from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework_api_key.permissions import HasAPIAccess

from ..algorithms import update_prof


@api_view(['POST'])
@permission_classes((HasAPIAccess, ))
def update_profile(request, username, *args, **kwargs):

    message = update_prof(request, username)

    return Response({"message": message})
