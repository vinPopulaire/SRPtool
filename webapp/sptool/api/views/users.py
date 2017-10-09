from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.algorithms import find_representatives
from api.models import Term
from api.models import User, UserContentScore
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
        terms = Term.objects.all()
        for term in terms:
            user_score = UserContentScore(
                    user_id=user.id,
                    term_id=term.id,
                    score=0
                    )
            user_score.save()
        return response


@api_view(['POST'])
def target(request, *args, **kwargs):

    representatives = find_representatives(request)

    terms = Term.objects.all().order_by('pk')

    # create json output of representatives with terms
    reps = {}
    for i in range(0, len(representatives)):
        rep = {}
        for j in range(0, len(terms)):
            rep[terms[j].term] = representatives[i][j]
        reps['representative %d' % (i+1)] = rep

    if representatives:
        response = Response(reps)
    else:
        response = Response({"message": "no information on target group"})

    return response
