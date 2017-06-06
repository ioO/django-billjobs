from billjobs.tests.generics import GenericAPIStatusCode

class GroupAPIAnonymousStatusCode(GenericAPIStatusCode):
    """
    Tests status code returned by /groups endpoint for anonymous user
    Permissions are tested in tests_api.py
    """

    def setUp(self):
        super().setUp()
