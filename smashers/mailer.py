from smtplib import SMTP
from smtplib import SMTPException
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
 
#Global varialbes
PASSWORD = "perfectlyvalidpassword"
EMAIL_SENDER  =  'jumbosmashers@gmail.com'
GMAIL_SMTP = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
TEXT_SUBTYPE = "html"

def containsnonasciicharacters(str):
    return not all(ord(c) < 128 for c in str)   

def addheader(message, headername, headervalue):
    if containsnonasciicharacters(headervalue):
        h = Header(headervalue, 'utf-8')
        message[headername] = h
    else:
        message[headername] = headervalue    
    return message

 
def listToStr(lst):
    """This method makes comma separated list item string"""
    return ','.join(lst)
 
def send_email(to, subject, content):
    """This method sends an email"""    
     
    #Create the message
    msg = MIMEMultipart('alternative')
    msg = addheader(msg, 'Subject', subject)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = listToStr(to)
    content = MIMEText(content.encode('utf-8'), "html")
    msg.attach(content);
     
    try:
      smtpObj = SMTP(GMAIL_SMTP, GMAIL_SMTP_PORT)
      #Identify yourself to GMAIL ESMTP server.
      smtpObj.ehlo()
      #Put SMTP connection in TLS mode and call ehlo again.
      smtpObj.starttls()
      smtpObj.ehlo()
      #Login to service
      smtpObj.login(user=EMAIL_SENDER, password=PASSWORD)
      #Send email
      print msg.as_string()
      smtpObj.sendmail(EMAIL_SENDER, to, msg.as_string())
      #close connection and session.
      smtpObj.quit();
    except SMTPException as error:
      print "Error: unable to send email :  {err}".format(err=error)
 
 
