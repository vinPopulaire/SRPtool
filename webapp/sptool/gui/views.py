import requests
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate

from .forms import SignupForm, ProfileForm, BusinessForm


def videos(request):
    current_user = request.user
    context = {}

    if current_user.is_authenticated():
        response = requests.post("http://davinci.netmode.ntua.gr/api/user/" + str(current_user) + "/recommend_videos",
                                 data={"num": 10}
                                 )
        videos_list = []
        for video in response.json()["videos"]:
            euscreen = video["video"]
            vid = requests.get("http://davinci.netmode.ntua.gr/api/video/" + str(euscreen)).json()
            videos_list.append({
                "title": vid["title"],
                "summary": vid["summary"],
                "euscreen": vid["euscreen"],
            })
        context = {"videos": videos_list}

    return render(request, 'gui/videos.html', context)


def play_video(request, euscreen, *args, **kwargs):
    current_user = request.user
    context = {}

    if current_user.is_authenticated():
        video = requests.get("http://davinci.netmode.ntua.gr/api/video/" + str(euscreen)).json()

        r = requests.post("http://davinci.netmode.ntua.gr/api/user/" + str(current_user) + "/watch",
                          data={"euscreen": str(euscreen)})

        enrichments = requests.post("http://davinci.netmode.ntua.gr/api/user/" + str(current_user) + "/recommend_enrichments",
                                    data={"euscreen": str(euscreen),
                                          "num": 0})

        enrichments_list = []
        for enrichment in enrichments.json()["enrichments"]:
            enrichment_id = enrichment["id"]
            enrich = requests.get("http://davinci.netmode.ntua.gr/api/enrichment/" + str(enrichment_id) + "/").json()
            enrichments_list.append({
                "frame": enrichment["frame"],
                "enrichment_id": enrich["enrichment_id"],
                "longName": enrich["longName"],
                "dbpedia": enrich["dbpediaURL"],
                "wikipedia": enrich["wikipediaURL"],
                "description": enrich["description"],
                "thumbnail": enrich["thumbnail"]
            })
        enrichments_list = sorted(enrichments_list, key=lambda x: x["frame"], reverse=False)
        context = {"video": video, "enrichments": enrichments_list}

    return render(request, 'gui/play.html', context)


def business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)

        if form.is_valid():

            data = {}

            age = form.cleaned_data.get('age')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            occupation = form.cleaned_data.get('occupation')
            education = form.cleaned_data.get('education')

            if age:
                data["age_id"] = age
            if gender:
                data["gender_id"] = gender
            if country:
                data["country_id"] = country
            if occupation:
                data["occupation_id"] = occupation
            if education:
                data["education_id"] = education

            response = requests.post("http://davinci.netmode.ntua.gr/api/videos_to_target",
                                     data=data
                                     ).json()

            first_representative = response["representative 1"]

            videos_list = []
            for video in first_representative:
                euscreen = video["video"]
                vid = requests.get("http://davinci.netmode.ntua.gr/api/video/" + str(euscreen)).json()
                videos_list.append({
                    "title": vid["title"],
                    "summary": vid["summary"],
                    "euscreen": vid["euscreen"],
                })

            enrichments_list = []

    else:
        form = BusinessForm()

        videos_list = []
        enrichments_list = []

    context = {'form': form, 'videos': videos_list, 'enrichments': enrichments_list}

    return render(request, 'gui/business.html', context)


def profile(request):
    current_user = request.user
    context = {}

    if current_user.is_authenticated():
        current_profile = requests.get("http://davinci.netmode.ntua.gr/api/user/" + str(current_user) + "/").json()

        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('first_name')
                surname = form.cleaned_data.get('last_name')
                age = form.cleaned_data.get('age')
                gender = form.cleaned_data.get('gender')
                country = form.cleaned_data.get('country')
                occupation = form.cleaned_data.get('occupation')
                education = form.cleaned_data.get('education')

                r = requests.put("http://davinci.netmode.ntua.gr/api/user/" + str(current_user) + "/",
                                 data={'username': current_profile["username"],
                                       'email': current_profile["email"],
                                       'name': name,
                                       'surname': surname,
                                       'age': age,
                                       'gender': gender,
                                       'country': country,
                                       'occupation': occupation,
                                       'education': education})

                return redirect('profile')
        else:
            form = ProfileForm(initial={'first_name': current_profile["name"],
                                        'last_name': current_profile["surname"],
                                        'age': current_profile["age"],
                                        'gender': current_profile["gender"],
                                        'country': current_profile["country"],
                                        'occupation': current_profile["occupation"],
                                        'education': current_profile["education"]})

        context = {'form': form}

    return render(request, 'gui/profile.html', context)


def delete(request):
    current_user = request.user

    if current_user.is_authenticated:
        # delete platform user
        r = requests.delete("http://davinci.netmode.ntua.gr/api/user/" + str(current_user))

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

            r = requests.post("http://davinci.netmode.ntua.gr/api/user/",
                              data={'username': username,
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


def home(request, *args, **kwargs):

    context = {}

    return render(request, 'gui/home.html', context)


def terms(request, *args, **kwargs):
    context = {}

    return render(request, 'gui/terms.html', context)


def about(request, *args, **kwargs):
    context = {}

    return render(request, 'gui/about.html', context)
