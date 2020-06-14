class EmailRecipient:

    first_name = ''
    last_name = ''
    address = ''
    address2 = ''
    city = ''
    state = ''
    zip = ''
    email = ''
    sex = ''
    age = 0
    mailing_list = False
    aarc_member = False
    number_of_contacts = 0
    most_recent_contact = ''
    emails_sent = 0
    emails_opened = 0
    opted_out = False
    opt_out_date = ''

    def __init__(self):
        pass

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name}({self.email!r})'

    def __str__(self):
        return str(self.email)

