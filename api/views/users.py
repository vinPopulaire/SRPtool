from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from api.models import User, UserContentScore
from api.models import Term
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = "username"

    def create(self, request, *args, **kwargs):
        # create user object
        response = super(UserViewSet, self).create(request, *args, **kwargs)

        # initialize user's content score
        user = User.objects.get(username=request.data["username"])
        term_list = Term.objects.all()
        for term in term_list:
            user_score = UserContentScore(
                    user_id = user.id,
                    term_id = term.id,
                    score = 0
                    )
            user_score.save()
        return response


@api_view(['POST'])
def representative(request, *args, **kwargs):

    message = "ok"

    return Response({"representatives": message})
