import requests
from django.conf import settings
import re
import json
import hashlib
MAILCHIMP_API_KEY = getattr(settings,"MAILCHIMP_API_KEY",None)
MAILCHIMP_DATA_CENTER = getattr(settings,"MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings,"MAILCHIMP_EMAIL_LIST_ID",None)

class Mailchimp(object):
    def __init__(self):
        super().__init__()
        self.key=MAILCHIMP_API_KEY
        self.dc=MAILCHIMP_DATA_CENTER
        self.list_url="https://{}.api.mailchimp.com/3.0".format(self.dc)
        self.list_id=MAILCHIMP_EMAIL_LIST_ID

    def check_email(self,email):
        if not re.match(r".+@.+\..+", email):
            raise ValueError('String passed is not a valid email address')
        return

    def check_status(self,status):
        choices=('subscribed','unsubscribed','cleaned','pending')

        if status not in choices:
            raise ValueError("status is not correct")
        return status

    def hash_email(self,email):               # hash ??
        '''
            This makes a email hash which is required by the Mailchimp API
            '''
        self.check_email(email)
        member_email = email.lower().encode()
        m = hashlib.md5(member_email)
        return m.hexdigest()


    def get_endpoint(self):
        return self.list_url+"/lists/"+self.list_id+"/members"


    def add_email(self,email):
        self.check_email(email)
        endpoint=self.get_endpoint()
        auth=("",MAILCHIMP_API_KEY)     # auth ??  --> auth take 2 arguments user and password
        status='subscribed'
        # self.check_status(status)
        data={
            "email_address":email,
            "status":self.check_status(status)
        }
        r=requests.post(endpoint,auth=auth,data=json.dumps(data))
        return r.status_code,r.json()


    def change_status(self,email,status):
        self.check_email(email)
        endpoint = self.get_endpoint() + "/" + self.hash_email(email)
        auth = ("", MAILCHIMP_API_KEY)  # auth ??
        # status = 'unsubscribed'

        data = {
            "email_address": email,
            "status": self.check_status(status)
        }
        r = requests.put(endpoint, auth=auth, data=json.dumps(data))
        return r.status_code,r.json()

    def check_user(self,email):
        self.check_email(email)
        endpoint = self.get_endpoint() + "/" + self.hash_email(email)
        auth = ("", MAILCHIMP_API_KEY)  # auth ??
        r = requests.put(endpoint, auth=auth)
        return r.status_code, r.json()

    def unsubscribed(self,email):
        return self.change_status(email,"unsubscribed")

    def subscribed(self,email):
        return self.change_status(email,"subscribed")

    def pending(self,email):
        return self.change_status(email,"pending")

