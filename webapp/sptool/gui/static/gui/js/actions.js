// TODO remove print logs for production

function PlayAction(user, video, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/actions", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var data = JSON.stringify({
        "euscreen": video["euscreen"].toString(),
        "action": "play_video",
        "time" : "1"});

    // console.log(csrftoken);
    xhttp.send(data);
    console.log(video["euscreen"]);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}

function StopAction(user, video, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/actions", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var data = JSON.stringify({
        "euscreen": video["euscreen"].toString(),
        "action": "stop_video",
        "time" : "10",
        "duration": "20"});

    xhttp.send(data);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}

function ClickEnrichmentAction(user, video, enrichment, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/actions", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var data = JSON.stringify({
        "euscreen": video["euscreen"].toString(),
        "action": "click_enrichment",
        "enrichment_id": enrichment.enrichment_id.toString()});

    xhttp.send(data);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}

function ShareAction(user, video, site_url) {
    console.log("Not implemented yet")
}

// TODO change "share" action to "share_enrichment" on Actions model
function ShareEnrichmentAction(user, video, enrichment, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/actions", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var data = JSON.stringify({
        "euscreen": video["euscreen"].toString(),
        "action": "share",
        "enrichment_id": enrichment.enrichment_id.toString()});

    xhttp.send(data);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}

function LikeAction(user, video, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/actions", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var data = JSON.stringify({
        "euscreen": video["euscreen"].toString(),
        "action": "explicit_rf",
        "value": 1});

    xhttp.send(data);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}

function DislikeAction(user, video, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/actions", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    var data = JSON.stringify({
        "euscreen": video["euscreen"].toString(),
        "action": "explicit_rf",
        "value": -1});

    xhttp.send(data);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}

function UpdateProfile(user, video_euscreen, site_url) {
    var csrftoken = Cookies.get('csrftoken');
    var xhttp = new XMLHttpRequest();
    // open(method, url, asynchronous)
    console.log("Update profile started");
    xhttp.open("POST", site_url.toString() + "/api/user/" + user.toString() + "/update_profile", false);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);

    var data = JSON.stringify({
        "euscreen": video_euscreen});

    xhttp.send(data);
    var response = JSON.parse(xhttp.responseText);
    console.log(response);
}
