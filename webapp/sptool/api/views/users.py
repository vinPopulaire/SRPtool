from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..algorithms import find_representatives
from ..models import Term
from ..models import User, UserContentScore
from ..serializers import UserSerializer


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

    clusters = find_representatives(request)

    if clusters:
        terms = Term.objects.all().order_by('pk')

        # create json output of representatives with terms
        reps = {}
        i = 1
        for key, value in clusters.items():
            ter = {}
            for j in range(0, len(terms)):
                ter[terms[j].term] = value["representative"][j]
            rep = {
                "terms": ter,
                "num_of_members": value["num_of_members"]
            }
            reps['representative %d' % i] = rep
            i = i+1
        response = Response(reps)
    else:
        response = Response({"message": "no information on target group"})

    return response
