from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json
import io

class GenericAPI(TestCase):
    """
    A generic class for API test
    """
    fixtures=['test_api_user.yaml']

    def setUp(self):
        """
        Common vars for tests
        """
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.client = APIClient()
        self.endpoints = {
                'api-token-auth': self.endpoint_url('api-token-auth'),
                'users': self.endpoint_url('users-api'),
                'users-detail': self.endpoint_url(
                    'users-detail-api', args=(3,))
                }
        self.url_users_detail = reverse('users-detail-api', args=(1,))

    def force_authenticate(self, user):
        """
        Force authenticate of client with user

        Parameters
        ----------
        user : Object
            A django.contrib.models.User instance
        """
        self.client.force_authenticate(user=user)

    def endpoint_url(self, urlname, args=None):
        """
        Return url endpoint

        Parameters
        ----------
        urlname : string
            The name of the pattern in urls.py
        args: list
            A list of arguments for the url

        Returns
        -------
        The uri for the test client
        """
        if args is not None:
            return reverse(urlname, args=args)
        else:
            return reverse(urlname)

    def get_response(self, method, url, data=None):
        """
        Get a response from client

        Parameters
        ----------
        method : string
            The http method to use for the request
        url : string
            The target url for the request
        data : dict
            A dictionary of data to add in request (POST, PUT)

        Returns
        -------
        A response from APIClient()
        """
        if method == 'GET':
            response = self.client.get(url, format='json')

        elif method == 'POST':
            response = self.client.post(url, data, format='json')

        elif method == 'PUT':
            response = self.client.put(url, data, format='json')

        elif method == 'DELETE':
            response = self.client.delete(url, format='json')

        return response

class GenericAPIStatusCode(GenericAPI):
    """
    A generic class to test status code returned by API
    """

    def status_code_is(self, method, url, data, status_code):
        response = super().get_response(method, url, data)
        self.assertEqual(response.status_code, status_code)

class GenericAPIResponseContent(GenericAPI):
    """
    A generic class to test response content from api
    """

    def get_json(self, method, url, data=None):
        """
        Get a json from a response

        Parameters
        ----------
        method : string
            The http method to use for the request
        url : string
            The target url for the request
        data : dict
            A dictionary of data to add in request (POST, PUT)

        Return
        ------
        A deserialized json in python
        """
        if method == 'GET':
            response = self.client.get(url, format='json')

        elif method == 'POST':
            response = self.client.post(url, data, format='json')

        elif method == 'PUT':
            response = self.client.put(url, data, format='json')

        elif method == 'DELETE':
            response = self.client.delete(url, format='json')


        return json.load(io.StringIO(response.content.decode()))


