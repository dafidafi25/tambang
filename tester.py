from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
subject = "My Subject"
html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
sender = {"name":"dafi","email":"dafidafi25@gmail.com"}
to = [{"email":"dafisteam25@gmail.com","name":"dafi"}]
reply_to = {"email":"replyto@domain.com","name":"John Doe"}
headers = {"Some-Custom-Name":"unique-id-1234"}
params = {"parameter":"My param value","subject":"New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)