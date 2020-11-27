from flask import current_app, render_template
import requests

def send_activate_mail(user):
    requests.post(current_app.config['MAIL_BASE_URL'], auth=('api', current_app.config['MAIL_API_KEY']),
    files=[("inline", open('images/favicon/link.png', 'rb'))],
    data={"from": "{0} {1}".format(current_app.config['MAIL_FROM'], current_app.config['MAIL_FROM_URL']),
    "to": [user.email], "subject": 'Confirm your Email',
    "html": render_template('activate.html', user=user, client_url=current_app.config['CLIENT_URL'])})

def send_password_reset_mail(user, reset):
    requests.post(current_app.config['MAIL_BASE_URL'], auth=('api', current_app.config['MAIL_API_KEY']),
    files=[('inline', open('images/favicon/link.png', 'rb'))],
    data={'from':"{0} {1}".format(current_app.config['MAIL_FROM'], current_app.config['MAIL_FROM_URL']),
    'to':[user.email], 'subject':'Change your Trim Password', 
    'html':render_template('reset_password.html', name=user.name, client_url=current_app.config['CLIENT_URL'], 
    reset=reset)})