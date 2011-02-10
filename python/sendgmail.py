#!/bin/env python
#-*- coding: UTF-8 -*-
import os,sys
import getopt
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from  subprocess import *

def sendgmail(username,password,mailfrom,mailto,subject,content):
    gserver = 'smtp.gmail.com'
    gport = 587

    msg = MIMEMultipart()
    msg['from'] = mailfrom
    msg['to'] = mailto
    msg['Reply-To'] = mailfrom
    msg['Subject'] = subject
    msg.attach(MIMEText(content))

    smtp = smtplib.SMTP(gserver, gport)
    smtp.set_debuglevel(0)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username,password)

    smtp.sendmail(mailfrom, mailto, msg.as_string())
    smtp.close()


    smtp.sendmail(mailfrom, mailto, msg.as_string())
    smtp.close()


def usage():
    print """
Usage: sendgmail -t [rcptto] -s [sbuject] [read from pipe]
E.g.: cat msg | ./sendgmail -t test@test.com -s testmail

"""

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:ho:v", ["to", "subject", "help", "output="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    verbose = False
    to= ""
    title= "untitled"
    content= ""

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-t", "--to"):
            to = a
        elif o in ("-s", "--subject"):
            subject = a
        else:
            assert False, "unhandled option"
    # ...

    for line in sys.stdin.readlines():
        content = content + line

    if to=="":
        usage()
        sys.exit()
    sendgmail('gmailaccount','password','mailfrom',to,subject,content)

if __name__ == "__main__":
    main()


