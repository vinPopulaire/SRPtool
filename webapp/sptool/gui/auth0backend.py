import requests
from social_core.backends.oauth import BaseOAuth2
from social_core.utils import handle_http_errors
from social_core.exceptions import AuthFailed
from django.shortcuts import redirect

import json


class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture')
    ]

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        try:
            self.process_error(self.data)
            state = self.validate_state()

            response = self.request_access_token(
                self.access_token_url(),
                data=self.auth_complete_params(state),
                headers=self.auth_headers(),
                auth=self.auth_complete_credentials(),
                method=self.ACCESS_TOKEN_METHOD
            )
            self.process_error(response)

            details = self.get_user_details(response)
            user_dict = json.loads(details["user"])
            user_type = user_dict["userType"]
            if user_type != 'Producer':
                data = {"error":"denied"}
                raise AuthFailed(self, data)
        except AuthFailed:
            return redirect('http://producer-toolkit.eu')
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    def auth_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        params = {
            'client_id': client_id,
            'redirect_uri': self.get_redirect_uri(state),
            'prompt': 'none'
        }
        if self.STATE_PARAMETER and state:
            params['state'] = state
        if self.RESPONSE_TYPE:
            params['response_type'] = self.RESPONSE_TYPE
        return params

    def authorization_url(self):
        """Return the authorization endpoint."""
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        """Return the token endpoint."""
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()

        return {'username': userinfo['nickname'],
                'first_name': userinfo['name'],
                'picture': userinfo['picture'],
                'user_id': userinfo['sub'],
                'user': userinfo['https://producer.eu/user_metadata']['user']}