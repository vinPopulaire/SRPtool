import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, ProfileForm, BusinessForm

from django.apps import apps

import os
import csv, json


@login_required
def videos(request):
    current_user = request.user

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

    response = requests.post(site_url + "/api/user/" + str(current_user) + "/recommend_videos",
                             data={"num": 10},
                             headers={
                                 "Api-Key": api_key,
                             },
                             )
    recommended_videos_list = []
    for video in response.json()["videos"]:
        euscreen = video["video"]
        vid = requests.get(site_url + "/api/video/" + str(euscreen),
                           headers={
                               "Api-Key": api_key,
                           },
                           ).json()
        recommended_videos_list.append({
            "title": vid["title"],
            "summary": vid["summary"],
            "euscreen": vid["euscreen"],
        })

    context = {"recommended_videos": recommended_videos_list, "site_url": site_url, "api_key": api_key}

    return render(request, 'gui/videos.html', context)


@login_required
def play_video(request, euscreen, *args, **kwargs):
    current_user = request.user

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

    video = requests.get(site_url + "/api/video/" + str(euscreen),
                         headers={
                             "Api-Key": api_key,
                         },
                         ).json()

    r = requests.post(site_url + "/api/user/" + str(current_user) + "/watch",
                      data={"euscreen": str(euscreen)},
                      headers={
                          "Api-Key": api_key,
                      },
                      )

    enrichments = requests.post(site_url + "/api/user/" + str(current_user) + "/recommend_enrichments",
                                data={"euscreen": str(euscreen),
                                      "num": 0},
                                headers={
                                    "Api-Key": api_key,
                                },
                                )

    enrichments_list = []
    for enrichment in enrichments.json()["enrichments"]:
        enrichment_id = enrichment["id"]
        enrich = requests.get(site_url + "/api/enrichment/" + str(enrichment_id) + "/",
                              headers={
                                  "Api-Key": api_key,
                              },
                              ).json()
        enrichments_list.append({
            "time": enrichment["start_time"],
            "enrichment_id": enrich["enrichment_id"],
            "name": enrich["name"],
            "thumbnail": enrich["thumbnail"],
            "title": enrich["title"],
            "overlay_title": enrich["overlay_title"],
            "overlay_text_description": enrich["overlay_text_description"],
        })
    enrichments_list = sorted(enrichments_list, key=lambda x: x["time"], reverse=False)
    context = {"video": video, "enrichments": enrichments_list, "site_url": site_url, "api_key": api_key}

    return render(request, 'gui/play.html', context)


@login_required
def business(request):

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

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

            response = requests.post(site_url + "/api/videos_to_target",
                                     data=data,
                                     headers={
                                         "Api-Key": api_key,
                                     },
                                     ).json()

            videos_list = []

            if "representative 1" in response:
                max_num_cluster = 0
                for representative in response:
                    if response[representative]["num_of_members"] > max_num_cluster:
                        max_num_cluster = response[representative]["num_of_members"]
                        max_representative = representative

                representative = response[max_representative]
                rep_videos = representative["videos"]

                for video in rep_videos:
                    euscreen = video["video"]
                    vid = requests.get(site_url + "/api/video/" + str(euscreen),
                                       headers={
                                           "Api-Key": api_key,
                                       },
                                       ).json()
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

    context = {'form': form, 'videos': videos_list, 'enrichments': enrichments_list, 'site_url': site_url, "api_key": api_key}

    return render(request, 'gui/business.html', context)


@login_required
def profile(request):
    current_user = request.user

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

    current_profile = requests.get(site_url + "/api/user/" + str(current_user) + "/",
                                   headers={
                                       "Api-Key": api_key,
                                   },
                                   ).json()

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

            r = requests.put(site_url + "/api/user/" + str(current_user) + "/",
                             data={'username': current_profile["username"],
                                   'email': current_profile["email"],
                                   'name': name,
                                   'surname': surname,
                                   'age': age,
                                   'gender': gender,
                                   'country': country,
                                   'occupation': occupation,
                                   'education': education},
                             headers={
                                 "Api-Key": api_key,
                             },
                             )

            return redirect('profile')
    else:
        form = ProfileForm(initial={'first_name': current_profile["name"],
                                    'last_name': current_profile["surname"],
                                    'age': current_profile["age"],
                                    'gender': current_profile["gender"],
                                    'country': current_profile["country"],
                                    'occupation': current_profile["occupation"],
                                    'education': current_profile["education"]})

    # workaround to get the user_vector for benchmarking
    User = apps.get_model('api', 'User')
    user = User.objects.get(username=current_user)

    Term = apps.get_model('api', 'Term')
    terms = Term.objects.all().order_by('id').values_list('term', flat=True)

    user_vector = user.get_user_vector()

    vectors = zip(terms, user_vector)

    context = {'form': form, 'vectors': vectors}

    return render(request, 'gui/profile.html', context)


@login_required
def delete(request):
    current_user = request.user

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

    # delete platform user
    r = requests.delete(site_url + "/api/user/" + str(current_user),
                        headers={
                            "Api-Key": api_key,
                        },
                        )

    # delete gui user
    current_user.delete()

    return redirect('home')


def signup(request):

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

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

            r = requests.post(site_url + "/api/user/",
                              data={'username': username,
                                    'email': email,
                                    'name': name,
                                    'surname': surname,
                                    'age': age,
                                    'gender': gender,
                                    'country': country,
                                    'occupation': occupation,
                                    'education': education},
                              headers={
                                  "Api-Key": api_key,
                              },
                              )

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


@login_required
def export(request, *args, **kwargs):

    site_url = os.environ.get("SITE_URL")
    api_key = os.environ.get("API_KEY")

    if request.method == 'POST':
        # gives list of id of inputs
        checked_enrichments = request.POST.getlist('checked')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enrichments.csv"'

        writer = csv.writer(response)

        writer.writerow(['Frame', 'Enrichment_id', 'Class', 'Title', 'Name', 'DBpedia', 'Wikipedia', 'Overlay Title', 'Description'])

        for item in checked_enrichments:

            data = item.split("@")
            enrichment_id = data[0]
            time = data[1]

            enrich = requests.get(site_url + "/api/enrichment/" + str(enrichment_id) + "/",
                                  headers={
                                      "Api-Key": api_key,
                                  },
                                  ).json()

            print(enrich)

            writer.writerow([time, enrich["enrichment_id"], enrich["enrichment_class"], enrich["title"], enrich["name"], enrich["dbpediaURL"], enrich["wikipediaURL"], enrich["overlay_title"], enrich["overlay_text_description"]])

        return response

    return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider="auth0")
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }

    context = {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    }

    return render(request, 'gui/dashboard.html', context)