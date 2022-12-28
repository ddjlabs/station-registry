import csv
import os
import time

from django.test import Client, TransactionTestCase

# Constants
C_BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_test_data(unit_test_number: int, data):
    try:
        for x in data:
            if int(x["unittest_case_number"]) == unit_test_number:
                return x
        return None
    except Exception as err:
        raise err


class RegisterCGITests(TransactionTestCase):
    fixtures = ['station_status.json', 'url_blacklist.json']
    testdata = {}
    C_REGISTER_CGI_ENDPOINT = '/register/register.cgi'
    C_CLIENT_PRIVATE_SETUP = {'HTTP_USER_AGENT': 'firefox-22', 'REMOTE_ADDR': '192.168.200.200'}
    C_CLIENT_PUBLIC_SETUP = {'HTTP_USER_AGENT': 'firefox-22', 'REMOTE_ADDR': '47.201.2.19'}

    def setUp(self):
        self.client = Client()

        s_filename = os.path.join(C_BASE_DIR, 'stationregistry', 'unit_test_data.csv')
        with open(s_filename, mode='r') as file:
            self.testdata = list(csv.DictReader(file, delimiter='|'))

    def tearDown(self):
        self.client = None

    def test_get_method_entry(self):
        """
        Unit Test#1 Test a simple GET using the Django test client agains the register CGI Endpoint.
        
        PASS = Record was accepted and loaded into the station_entries and stations table.
        """

        o_data = get_test_data(1, self.testdata)

        response = self.client.get(self.C_REGISTER_CGI_ENDPOINT, o_data, **self.C_CLIENT_PUBLIC_SETUP)
        self.assertEqual(response.status_code, 200)

    def test_post_method_entry(self):
        """
        Unit Test#2 Test a simple POST using the Django test client agains the register CGI Endpoint.
        
        PASS = Record was accepted and loaded into the station_entries and stations table.
        """

        o_data = get_test_data(1, self.testdata)

        response = self.client.post(self.C_REGISTER_CGI_ENDPOINT, o_data, **self.C_CLIENT_PUBLIC_SETUP)
        self.assertEqual(response.status_code, 200)

    def test_private_url_post_entry(self):
        """
        Unit Test#3 Test using a private IP Address (192.168.10.1) as a station URL.
        
        PASS = Record will be rejected with a 405 bad request
        TESTCASE#2
        """

        o_data = get_test_data(2, self.testdata)

        response = self.client.post(self.C_REGISTER_CGI_ENDPOINT, o_data, **self.C_CLIENT_PUBLIC_SETUP)
        self.assertEqual(response.status_code, 400)

    def test_bad_url_post_entry(self):
        """
        Unit Test#4 Test using a known bad URL (WeeWx.com) as a station URL.
        
        PASS = Record will be rejected as it will be in the URLBlackList table.
        TESTCASE#3
        """

        o_data = get_test_data(3, self.testdata)

        response = self.client.post(self.C_REGISTER_CGI_ENDPOINT, o_data, **self.C_CLIENT_PUBLIC_SETUP)
        self.assertEqual(response.status_code, 400)

    def test_bad_url_post_entry2(self):
        """
        Unit Test#4 Test using a known bad URL (WeeWx.com) as a station URL.
        
        PASS = Record will be rejected as it will be in the URLBlackList table.
        TESTCASE#3
        """

        o_data = get_test_data(4, self.testdata)

        response = self.client.post(self.C_REGISTER_CGI_ENDPOINT, o_data, **self.C_CLIENT_PUBLIC_SETUP)
        self.assertEqual(response.status_code, 400)

    def test_update_existing_entry(self):
        """
        Unit Test#5 Update existing record with some small update after 1 minute
        
        PASS = Record will be accepted. It will create a station_entry record for the update and re-update stations table.
        TESTCASE#5
        """

        o_data = get_test_data(1, self.testdata)

        r1 = self.client.post(self.C_REGISTER_CGI_ENDPOINT, o_data, **self.C_CLIENT_PUBLIC_SETUP)

        # pause 1 minute
        time.sleep(30)

        o_data2 = get_test_data(5, self.testdata)

        response = self.client.post(self.C_REGISTER_CGI_ENDPOINT, o_data2, **self.C_CLIENT_PUBLIC_SETUP)

        # input('Woah Stop!')
        self.assertEqual(response.status_code, 200)
