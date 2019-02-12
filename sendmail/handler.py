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

    s = smtplib.SMTP(mailhost, 587)
    print(mailhost)
    s.set_debuglevel(1)
    s.starttls()
    s.login(me,pw)
    s.sendmail(me, you, msg.as_string())
    s.quit()

