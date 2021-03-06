import smtplib
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import namedtuple
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# https://docs.python.org/3.4/library/email-examples.html


def handle(req):
    mailadd = open("/var/openfaas/secrets/func-email", "r")
    mailpw = open("/var/openfaas/secrets/func-emailpw", "r")
    smtpadd = open("/var/openfaas/secrets/func-smtpaddress", "r")

    data=req
    x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    
    mailhost = smtpadd.read()
    me = mailadd.read()
    pw = mailpw.read()
    you = x.email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = x.subject
    msg['From'] = me
    msg['To'] = you

    text = x.text
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    try:
        s = smtplib.SMTP(mailhost, 587)
        s.set_debuglevel(x.level)
        s.starttls()
        s.login(me,pw)
        s.sendmail(me, you, msg.as_string())
        print('email sent')
        s.quit()
    except s.SMTPException:
        print('error')
        s.quit()


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response


if __name__ == '__main__':
    app.run()
