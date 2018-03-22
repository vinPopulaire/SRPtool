from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..algorithms import find_representatives
from ..models import Term
from ..models import User, UserContentScore, Friend
from ..serializers import UserSerializer
from ..algorithms import get_starting_vector

from django.contrib.auth.models import User as Auth_user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_value_regex = '[0-9 a-z.A-Z_]+'

    lookup_field = "username"

    def create(self, request, *args, **kwargs):
        # create user object
        response = super(UserViewSet, self).create(request, *args, **kwargs)

        # initialize user's content score
        user = User.objects.get(username=request.data["username"])
        terms = Term.objects.all()

        user_vector = get_starting_vector(user)

        for idx, term in enumerate(terms):
            user_score = UserContentScore(
                    user_id=user.id,
                    term_id=term.id,
                    score=user_vector[idx]
                    )
            user_score.save()
        return response

    def update(self, request, *args, **kwargs):
        response = super(UserViewSet, self).update(request, *args, **kwargs)

        instance = self.get_object()
        auth_user = Auth_user.objects.get(username=instance.username)

        if "name" in request.data:
            auth_user.first_name = request.data["name"]
        if "surname" in request.data:
            auth_user.last_name = request.data["surname"]

        auth_user.save()

        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username
        self.perform_destroy(instance)
        return Response({"message": "user " + username + " is successfully deleted"})


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


@api_view(['GET'])
def show_friends(request, username):
    user = User.objects.get(username=username)

    friends_names = user.get_friends_list()

    result = {
        "friends":friends_names
    }

    response = Response(result)

    return response


@api_view(['POST'])
def add_friend(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    if "friend" in request.data:
        friend = request.data["friend"]
    else:
        return Response({"message": "Friend user must be specified"})

    try:
        friend = User.objects.get(username=friend)
    except User.DoesNotExist:
        return Response({"message": "Friend user does not exist"})


    already_friends = Friend.objects.filter(user=user,friend=friend)
    if already_friends:
        return Response({"message": "%s is already friends with %s" % (user, friend)})

    Friend.objects.create(user=user,friend=friend)
    Friend.objects.create(user=friend, friend=user)

    response = Response({"message": "%s is now friends with %s" % (user, friend)})

    return response


@api_view(['POST'])
def remove_friend(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    if "friend" in request.data:
        friend = request.data["friend"]
    else:
        return Response({"message": "Friend user must be specified"})

    try:
        friend = User.objects.get(username=friend)
    except User.DoesNotExist:
        return Response({"message": "Friend user does not exist"})

    already_friends = Friend.objects.filter(user=user, friend=friend)
    if not already_friends:
        return Response({"message": "%s is not friends with %s yet" % (user, friend)})

    Friend.objects.filter(user=user,friend=friend).delete()
    Friend.objects.filter(user=friend, friend=user).delete()

    response = Response({"message": "%s is no longer friends with %s" % (user, friend)})

    return response
