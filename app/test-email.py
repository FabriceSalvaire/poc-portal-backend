####################################################################################################

# https://github.com/lavr/python-emails
# https://python-emails.readthedocs.io
import emails

####################################################################################################

sender = '...'

message = emails.Message(
    subject="Test",
    text="just a test",
    # html='',
    mail_from=("Fabrice", sender),
)
smtp_options = {
    "host": "smtp.orange.fr",
    "port": 25,
}
# smtp_options["tls"] = True
# smtp_options["user"] = ""
# smtp_options["password"] = ""

environment = {}
response = message.send(to=sender, render=environment, smtp=smtp_options)
print(response)
if response.status_code not in [250, ]:
    print('Failed')
