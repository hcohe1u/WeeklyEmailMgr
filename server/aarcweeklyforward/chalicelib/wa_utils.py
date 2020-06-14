from chalicelib.wa_api import WaApiClient
import json
import os, pickle
from smart_open import open
import tempfile
from urllib.parse import urlencode
from inspect import getmembers


DIR_PREFIX = "s3://aarclub-files/weekly-emails/" if 'AWS_REGION' in os.environ else ""
PICKLE_FILENAME = "wa_all_contacts.p"
STATS_FILENAME = "aarc_stats.json"


class WaUtils(object):


    wa_api = None

    def __init__(self):
        self.wa_api = self.wild_apricot_api()
#        self.aarc_stats = self.get_aarc_stats()
        return

    def wild_apricot_api(self):
        # How to obtain application credentials:
        # https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
        cred_file = open(f'{DIR_PREFIX}wa_credentials.json', 'rb')
        credentials = json.load(cred_file)
        api = WaApiClient(credentials['client_id'], credentials['client_secret'])
        #api.authenticate_with_apikey(credentials['api_key'])
        api.authenticate_with_contact_credentials(credentials['administrator_username'],
                                                credentials['administrator_password'])
        return api

    def refresh_aarc_stats(self):
        #if wa_api is None:
#        wa_api = wild_apricot_api()
    #    query_str = "/v2.2/accounts/30507/Contacts?$async=false&$filter='Membership+status.Id'+eq+1"
        query_str = "/v2.2/accounts/30507/Contacts?$async=false"
    # execute_request() returns a single API object holding list of contacts represented as API objects.
    # Each contact API object contains a dictionary of attributes
        contacts = [contact.__dict__ for contact in self.wa_api.execute_request(query_str).__dict__['Contacts']]
        members = [contact for contact in contacts if "Status" in contact and contact["Status"] == "Active"]

    # Dump to a file for local analysis
    #    pickle.dump(contacts, open(f'{self.DIR_PREFIX}{self.PICKLE_FILENAME}', "wb"))    

        response = {}
        response['entrants'] = 0
        response['members'] = len(members)
        response['contacts'] = len(contacts)
        try:
            f = open(f'{tempfile.gettempdir()}/{STATS_FILENAME}', 'w')
            json.dump(response, f, indent=2)
            f = open(f'{DIR_PREFIX}{STATS_FILENAME}', 'w')
            json.dump(response, f, indent=2)
        except ValueError:
            return {}
        return response


    def get_aarc_stats(self):
        try:
            f = open(f'{tempfile.gettempdir()}/{STATS_FILENAME}', 'r')
            print('get_aarc_stats found local file')
            return json.load(f)
        except FileNotFoundError:
            try:
                f2 = open(f'{DIR_PREFIX}{STATS_FILENAME}', 'r')
                print('get_aarc_stats found file on S3')
                stats = json.load(f2)
                f3 = open(f'{tempfile.gettempdir()}/{STATS_FILENAME}', 'w')
                json.dump(stats, f3, indent=2)
                return stats
            except FileNotFoundError:
                print('get_aarc_stats creating stats files')
                return self.refresh_aarc_stats()
        return {}

    def get_email_body(self):
        top_email_entries = 500
        emailLogUrl = "/v2/Accounts/30507/SentEmails"
        print(f'Retrieving first {top_email_entries} from {emailLogUrl}')
        params = {'$top': top_email_entries,
                '$async': 'false'}
        request_url = emailLogUrl + '?' + urlencode(params)
        print(request_url)
        emails = self.wa_api.execute_request(request_url).__dict__["Emails"]
        print(f'emails = {type(emails)} {len(emails)}')
        for apiobj in emails:
            email = apiobj.__dict__
#            print(f'email = {email["Type"]}, {email.keys()}')
            if email['Type'] == 'EmailBlast_Members':
                print(f'Found EmailBlast_Members for {email["SentDate"]}')
                if email['Subject'].startswith('AARC Weekly Update'):
                    response = self.wa_api.execute_request(email['Url']).__dict__
                    print(f'Found Weekly Email for {response["SentDate"]} body length: {len(response["Body"])}')
                    return response['Subject'], response['Body']
        return None, None
