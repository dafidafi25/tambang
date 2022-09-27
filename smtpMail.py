import mailslurp_client
# create a mailslurp configuration
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = '33fb2f48d350c49868e1526255bbffb6e0e12eca88ce940610734b66f5081fd'
with mailslurp_client.ApiClient(configuration) as api_client:
    # create an inbox
    inbox_controller = mailslurp_client.InboxControllerApi(api_client)
    inbox_1 = inbox_controller.create_inbox()
    inbox_2 = inbox_controller.create_inbox()

    # send email
    opts = mailslurp_client.SendEmailOptions()
    opts.to = 'dafidafi25@gmail.com'
    opts.subject = "Hello"
    opts.body = "Email content <strong>supports HTML</strong>"
    opts.is_html = True
    inbox_controller.send_email(inbox_1.id, send_email_options=opts)