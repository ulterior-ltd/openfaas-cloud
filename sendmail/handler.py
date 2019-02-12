import smtplib
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import namedtuple
# https://docs.python.org/3.4/library/email-examples.html


def handle(req):
    mailadd = open("/var/openfaas/secrets/func-email", "r")
    mailpw = open("/var/openfaas/secrets/func-emailpw", "r")
    smtpadd = open("/var/openfaas/secrets/func-smtpaddress", "r")

    data=req
    x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    me = mailadd.read()
    you = x.email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = x.subject
    msg['From'] = me
    msg['To'] = you

    text = x.text
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    s = smtplib.SMTP(smtpadd.read(), 587)
    s.starttls()
    s.login(mailadd.read(), mailpw.read())
    s.sendmail(me, you, msg.as_string())
    # logging.warning("Mail Send Successfully")
    s.quit()

