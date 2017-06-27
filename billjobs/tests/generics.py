from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
import json
import io

class GenericAPITest(APITestCase):
    """
    Generic TestCase class to test an API endpoint
    """
    fixtures = ['test_api_010_group.yaml', 'test_api_user.yaml']

    def setUp(self):
        self.url = None
        self.client = APIClient()
        self.superuser = User.objects.get(pk=1)
        self.admin = User.objects.get(pk=2)
        self.bill = User.objects.get(pk=3)
        self.steve = User.objects.get(pk=4)
        self.nogroupuser = User.objects.get(pk=5)
        self.data = {
                'create': None,
                'update': None,
                }
        self.expected_status = {
                'GET': None,
                'POST': None,
                'PUT': None,
                'DELETE': None,
                'OPTIONS': None,
                'HEAD': None,
                'PATCH': None,
                }
        self.expected_content = {
                'GET': None,
                'POST': None,
                'PUT': None,
                'DELETE': None,
                'OPTIONS': None,
                'HEAD': None,
                'PATCH': None,
                }
        self.error_message = {
                '401': {
                    'detail': 'Authentication credentials were not provided.'},
                '403': {
                    'detail':
                        'You do not have permission to perform this action.'},
                '405_GET': {'detail': 'Method "GET" not allowed.'},
                '405_POST': {'detail': 'Method "POST" not allowed.'},
                '405_PUT': {'detail': 'Method "PUT" not allowed.'},
                '405_DELETE': {'detail': 'Method "DELETE" not allowed.'},
                '405_PATCH': {'detail': 'Method "PATCH" not allowed.'},
                '405_OPTIONS': {'detail': 'Method "OPTIONS" not allowed.'},
                '405_HEAD': {'detail': 'Method "HEAD" not allowed.'},
                }

    def tearDown(self):
        """
        Delete variables after each test
        """
        del self.url, self.client, self.admin, self.bill, self.steve, \
                self.nogroupuser, self.data, self.expected_status, \
                self.expected_content

    def force_authenticate(self, user):
        """
        Force authenticate of client with user

        Parameters
        ----------
        user : Object
            A django.contrib.models.User instance
        """
        self.client.force_authenticate(user=user)

    def get_response(self, method):
        """
        Get a response from client

        Parameters
        ----------
        method : string
            The http method to use for the request

        Returns
        -------
        A response from APIClient()
        """

        if method == 'GET':
            response = self.client.get(self.url, format='json')
        elif method == 'POST':
            response = self.client.post(
                    self.url, self.data['create'], format='json')
        elif method == 'PUT':
            response = self.client.put(
                    self.url, self.data['update'], format='json')
        elif method == 'DELETE':
            response = self.client.delete(self.url, format='json')
        elif method == 'HEAD':
            response = self.client.head(self.url, format='json')
        elif method == 'OPTIONS':
            response = self.client.options(self.url, format='json')
        elif method == 'PATCH':
            response = self.client.patch(self.url, format='json')

        return response

    def status_code_is(self):
        for method, status_code in self.expected_status.items():
            with self.subTest(method=method, status_code=status_code):
                response = self.get_response(method)
                self.assertEqual(response.status_code, status_code,
                        '{0} method expected status code {1}'.format( method,
                            status_code)
                        )

    def content_is(self):
        """
        Assert expected content is in response.data
        """
        for method, content in self.expected_content.items():
            with self.subTest(method=method, content=content):
                response = self.get_response(method)
                if type(content) is list:
                    self.assertEqual(len(content), len(response.data))
                    for num in range(len(content)):
                        self.assertDictEqual(content[num-1], response.data[num-1])
                elif type(content) is dict:
                    for key, value in content.items():
                        self.assertEqual(response.data[key], value,
                                '{0} method expected key "{1}" value'.format(
                                    method, key)
                                )

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
                    'users-detail-api', args=(3,)),
                'groups': self.endpoint_url('groups-api'),
                'groups-detail': self.endpoint_url(
                    'groups-detail-api', args=(1,)),
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
        """
        Assert that the response.status_code and status_code are equal.

        Parameters
        ----------
        method : string
            The http method to use for the request
        url : string
            The target url for the request
        data : dict
            A dictionary of data to add in request (POST, PUT)
        status_code : int
            The integer representing the status code (2xx, 3xx, 4xx, 5xx)

        Returns
        -------
        The test failed or not.
        """
        response = super().get_response(method, url, data)
        self.assertEqual(response.status_code, status_code)

class GenericAPIResponseContent(GenericAPI):
    """
    A generic class to test response content from api
    """

    def setUp(self):
        super().setUp()
        self.user_keys = ('url', 'password', 'last_login', 'is_superuser',
                'username', 'first_name', 'last_name', 'email', 'is_staff',
                'is_active', 'date_joined', 'groups', 'user_permissions')

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
        response = super().get_response(method, url, data)
        return json.load(io.StringIO(response.content.decode()))


