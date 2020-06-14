from chalicelib.email_recipient import EmailRecipient
import pickle, os
from chalicelib.wa_api import WaApiClient
import ezgmail, urllib
from urllib.parse import urlencode
from email.mime.text import MIMEText
import tempfile, boto3

DIR_PREFIX = "s3://aarclub-files/weekly-emails/" if 'AWS_REGION' in os.environ else ""

# Mailing list management
# email_recipients contains the list of email addresses to relay messages.  It is created from:
#    race_registrants: runners who registered for AARC races on Run The Day and answered Yes to "Okay to send emails"
#    aarc_members: runners to exclude since they already receive emails from directly from AARC
#    opt_outs: runners who unsubscribed earlier
#
race_registrants = []
aarc_members = []
opt_outs = []
email_recipients = {}

# Short list for testing
email_recipients = { 'aarcky.penguin@yahoo.com': EmailRecipient(),
                     'hcohe1u@yahoo.com': EmailRecipient(),
                     'hcohe1u@gmail.com': EmailRecipient(),
                     'howard.cohen@email.com': EmailRecipient(), }

# Pickled dictionary containing email recipient addresses and tracking info
RECIPIENT_FILENAME = f'{DIR_PREFIX}weekly_email_recipients.p'


def read_email_recipient_file():
    if os.path.exists(RECIPIENT_FILENAME):
        return pickle.load(open(RECIPIENT_FILENAME, 'rb'))
    else:
        return None


def write_email_recipient_file(recipient_dict):
    pickle.dump(recipient_dict, open(RECIPIENT_FILENAME, 'wb'))


def filter_aarc_members(recipient_dict, member_dict):
    filtered = 0
    for runner_email in member_dict.keys():
        if runner_email in recipient_dict:
            recipient_dict.pop(runner_email)
            filtered += 1
    return filtered


def do_some_analytics(recipient_dict):
    hist = {}
    for runner in recipient_dict.values():
        if runner.number_of_contacts in hist:
            hist[runner.number_of_contacts] += 1
        else:
            hist[runner.number_of_contacts] = 1
    return
    

def send_test_email():
    s3 = boto3.client('s3')
    ezgmail.init(userId='ambler.area.running.club@gmail.com')
    print(f'Ezgmail initialized for {ezgmail.EMAIL_ADDRESS}')
    ezgmail.send('hcohe1u@gmail.com', 'Hello from AARC', 'Pop, pop, popsicle, Ice, ice, icecycle, Test, test, testing one two three')
    return True


def relay_email(wa_client):
    s3 = boto3.client('s3')
    ezgmail.init(userId='ambler.area.running.club@gmail.com')
    subject, body = wa_client.get_email_body()
    if subject is not None and body is not None:
        for email in email_recipients.keys():
            print(f'Sending {len(body)} chars to {email}')
            ezgmail.send(email, subject, MIMEText(body, 'html', 'utf-8'))
    return True

