from chalice import Chalice
import os, sys
import json
from chalicelib.race_registrations import process_race_registrations, get_registration_stats
from chalicelib.wa_utils import WaUtils
import chalicelib.emailer as emailer
import logging

app = Chalice(app_name='aarcweeklyforward')
app.api.cors = True

wa_client = WaUtils()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('wa_client initialized')

@app.route('/')
def index():
#    try:
#        local = not os.environ['AWS_REGION']
#    except:
#        pass
#    return {'hello': sys.path}
    return {'hello': 'aarc'}
#    env = os.environ
#    return json.dumps({key : env[key] for key in env})


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

@app.route('/club-contacts')
def club_contacts():
    response = wa_client.get_aarc_stats()
    return response

@app.route('/club-contacts/refresh', methods=['POST'])
def post_club_contacts():
    print('Updating club contacts')
    return wa_client.refresh_aarc_stats()

@app.route('/race-reg-contacts')
def race_reg_contacts():
    return json.dumps(get_registration_stats())

@app.route('/race-reg-contacts/refresh', methods=['POST'])
def post_race_reg_contacts():
    print('Updating race reg contacts')
    return process_race_registrations()

@app.route('/emails')
def emails():
    return {'relayed': '10',
    'last-date': '12-April-2020',
    'last-relayed': '11-May-2020',
    'total-sent' : 5010
    }


@app.route('/emails/refresh', methods=['POST'])
def post_emails():
    print('Updating email stats')
#    wa_client.get_email_body()
    return {'email-status' : 'Success'}


@app.route('/emails/relay', methods=['POST'])
def relay_emails():
    print('Initiating email relay')
    return {'email-status' : emailer.relay_email(wa_client)}


@app.route('/emails/send-test', methods=['POST'])
def send_test():
    print('Sending Test email')
    return {"status" : emailer.send_test_email()}
