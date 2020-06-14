import csv, json
from chalicelib.email_recipient import EmailRecipient
from smart_open import open as smart_open
import boto3
import tempfile

recipient_dict = {}

# Offsets into RTD's race registration .csv files.
FIRST_NAME_FIELD = 0
LAST_NAME_FIELD = 1
ADDRESS_FIELD = 2
ADDRESS2_FIELD = 3
CITY_FIELD = 4
STATE_FIELD = 5
ZIP_FIELD = 6
EMAIL_FIELD = 8
SEX_FIELD = 9
AGE_FIELD = 11
MAILING_LIST_FIELD = 37
REGISTRATION_DATE_FIELD = 38

FILE_PREFIX = 's3://aarclub-files/weekly-emails/race-regs/'

# Version using smart_open.  Unfortunately, Chalice does not create S3 permissions
# if boto3 is not used to access file.
# Edited permissions manually in IAM console and added parameters to .chalice/config.json:
#   "manage_iam_role" : "false",
#   "iam_role_arn" : "arn:aws:iam::961809614400:role/aarcweeklyforward-dev"

def get_registration_files():
    try:
        f = smart_open(f'{FILE_PREFIX}reg_files.json', 'rb')
        reg_files = json.load(f)['reg_files']
        return reg_files
    except FileNotFoundError:
        return None
    except ValueError:
        return None

"""
#Version using boto3 directly in an attempt to make Chalice create the proper permissions for S3
def get_registration_files():
    try:
        s3 = boto3.client('s3')
        #with open('reg_files.json', 'wb') as f:
        with tempfile.TemporaryFile() as f:
            s3.download_fileobj('aarclub-files', 'weekly-emails/race-regs/reg_files.json', f)
        f.seek(0)
        reg_files = json.load(f)['reg_files']
        return reg_files
    except FileNotFoundError:
        return None
    except ValueError:
        return None
"""

def add_rtd_registrations(filename):
    race_regs_file = smart_open(f'{FILE_PREFIX}{filename}')
    race_regs_reader = csv.reader(race_regs_file)
    race_regs_entries = list(race_regs_reader)

    for row in race_regs_entries[1:]:
        recipient = EmailRecipient()
        recipient.first_name = row[FIRST_NAME_FIELD]
        recipient.last_name = row[LAST_NAME_FIELD]
        recipient.address = row[ADDRESS_FIELD]
        recipient.address2 = row[ADDRESS2_FIELD]
        recipient.city = row[CITY_FIELD]
        recipient.state = row[STATE_FIELD]
        recipient.zip = row[ZIP_FIELD]
        recipient.email = row[EMAIL_FIELD]
        recipient.sex = row[SEX_FIELD]
        recipient.age = row[AGE_FIELD]
        recipient.mailing_list = row[MAILING_LIST_FIELD]
        recipient.most_recent_contact = row[REGISTRATION_DATE_FIELD]
        recipient.number_of_contacts = 1
        if recipient.mailing_list == 'Yes': # Did they opt-in for future emails?
            if recipient.email not in recipient_dict: # Add new email address or update existing one
                recipient_dict[recipient.email] = recipient
            else:
                recipient_dict[recipient.email].number_of_contacts += 1
                recipient_dict[recipient.email].most_recent_contact = recipient.most_recent_contact
    return

def process_race_registrations():
    registration_files = get_registration_files()

    for filename in registration_files:
        print(f'Processing file {filename}')
        add_rtd_registrations(filename)
        print(f'Total email addresses found: {len(recipient_dict)}')
    response = {}
    response['races'] = len(registration_files)
    response['members'] = 0
    response['contacts'] = len(recipient_dict)
    try:
        f = smart_open(f'{FILE_PREFIX}stats.json', 'w')
        json.dump(response, f, indent=2)
    except FileNotFoundError:
        pass
    except ValueError:
        pass
    return json.dumps(response)

#TODO: Create a summary statistics file for read_race_reg_stats()

def get_registration_stats():
    try:
        f = smart_open(f'{FILE_PREFIX}stats.json', 'r')
        stats = json.load(f)
        return stats
    except FileNotFoundError:
        return None
    except ValueError:
        return None

