import smtplib
import ssl
from email.message import EmailMessage


def sendemail(reciever,subject,link,msg,name):
    email_sender = 'binarybits809@gmail.com'
    email_password = 'qhwvfgnxephbtguy'
    email_receiver = reciever

    s1='Form from : '
    str1= msg
    str2="\n\n"
    str3="Form link : "
    str4=link
    body = s1+name+str2+str1+str2+str3+str4

    subject = subject

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())





#sendemail(sender=sender,reciever=reciever,apppass=apppass)
