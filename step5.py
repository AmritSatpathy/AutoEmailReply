import re
import pandas as pd
from step4 import *
import imaplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from values import *

def fetchname(x):
    your_string = re.sub('\W+', ' ', x)
    bad_chars = ['Hi Rekha']
    your_string = your_string.strip()
    for i in bad_chars:
        test_string = your_string.replace(i, '')
    your_search_word = "Hi"
    list_of_words = str(test_string).split()
    next_word = list_of_words[list_of_words.index(your_search_word) + 1]
    rem_char = [">"]
    for j in rem_char:
        last_word = next_word.replace(j, ' ')
    return last_word


def draft(fromaddr, toaddr, messagebody,cc, subject):
    message = MIMEMultipart('Mixed')
    message['Subject'] = subject
    message['From'] = fromaddr
    message['to'] = toaddr
    message['cc'] = cc
    # message['bcc'] = 'testbcc@test.com'
    message.attach(MIMEText(messagebody,'html'))
    server = imaplib.IMAP4_SSL('imap.gmail.com')
    server.login(username, password)
    print("Draft Send")
    server.append('[Gmail]/Drafts', '\Draft', imaplib.Time2Internaldate(time.time()), str(message).encode("utf-8"))
    server.logout()


def string():
    loaded = pd.read_csv("fromjson.csv", engine='python')
    check = pd.read_csv("predictedresult.csv")
    mergedStuff = pd.merge(loaded, check, on=['Subject'], how='inner')
    for i in mergedStuff.index:
        name = fetchname(mergedStuff['text/plain_x'][i])
        if mergedStuff['Label'][i] == 1:
            if thirdperson(mergedStuff["text/plain_y"][i]):
                checkcc, name1 = thirdperson(mergedStuff["text/plain_y"][i])
                if checkcc == 1:
                    if name:
                        if name1:
                            message = 'Hi ', name,",","""<pre><br>Thanks for connecting us with the team. <br><br>Hi """, name1, """ ,<br><br>Happy to e-meet you. <br><br>Do let me know when we can connect over a call. Here is a link to my calendar.<br><br><a href="https://calendly.com/i-am-the-red-tomato/15min">My Calender Link</a><br><br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br>+91 9930459453 """
                            messagebody = ''.join(message)

                elif checkcc == 2:
                    if name:
                        message = 'Hi ', name1 ,",","""<pre><br>Happy to e-meet you.  <br><br>Do let me know when we can connect over a call.<br><br>Here is a link to my calendar for a meeting at a convenient time of yours.<br><br><a href="https://calendly.com/i-am-the-red-tomato/15min">My Calender Link</a><br><br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br>+91 9930459453 """
                        messagebody = ''.join(message)
                toaddr = mergedStuff["From_y"][i]
                cc = ccvalue
                fromaddr = mergedStuff["To_y"][i]
                subject = mergedStuff["Subject"][i]
                draft(fromaddr, toaddr, messagebody, cc, subject)
            elif connect(mergedStuff["text/plain_y"][i]):
                number, email, name1, date = connect(mergedStuff["text/plain_y"][i])
                if date == 1:
                    if name:
                        # mark calender
                        message = 'Hi ', name,",","""<pre><br><br>Thanks for your response.<br><br>Surely, I will connect with you for a brief meeting. <br><br><br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br><br>+91 9930459453</pre>"""
                        messagebody = ''.join(message)

                elif date == 2:
                    if name:
                        message = 'Hi ', name,",","""<pre><br>Thanks for your response.<br><br>Please select a convenient meeting time by clicking the below calendar link.<br><br><a href="https://calendly.com/i-am-the-red-tomato/15min">My Calender Link</a><br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br>+91 9930459453 </pre>"""
                        messagebody = ''.join(message)

                elif date == 3:
                    if name:
                        message = 'Hi ', name,",","""<pre><br>Thanks for your response.<br><br>Please select a convenient meeting time by clicking the below calendar link.<br><br><a href="https://calendly.com/i-am-the-red-tomato/15min">My Calender Link</a><br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br>+91 9930459453 </pre>"""
                        messagebody = ''.join(message)
                fromaddr = mergedStuff["To_y"][i]
                toaddr = mergedStuff["From_y"][i]
                cc = ccvalue
                subject = mergedStuff["Subject"][i]
                draft(fromaddr, toaddr, messagebody, cc, subject)

            elif detail(mergedStuff["text/plain_y"][i]):
                message = 'Hi ',name,",","""<pre><br>Thanks for your response. <br><br>Enclosed is a brief presentation about our company and solutions offering.<br><br>Happy to connect with you at a time convenient of yours to discuss a solution fitment.<br><br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br>+91 9930459453 """
                messagebody = ''.join(message)
                fromaddr = mergedStuff["To_y"][i]
                toaddr = mergedStuff["From_y"][i]
                cc = ccvalue
                subject = mergedStuff["Subject"][i]
                draft(fromaddr, toaddr, messagebody, cc, subject)

        elif mergedStuff['Label'][i] == 0:
            if name:
                message = 'Hi ', name,",","""<pre><br>Surely, noted.<br><br>Feel free to connect with us in the future if you would like to explore our offerings.<br><br>Best,<br>Rekha Jain <br>Founder <br>www.jetleads.io <br>+91 9930459453 </pre>"""
                messagebody = ''.join(message)


            fromaddr = mergedStuff["To_y"][i]
            toaddr = mergedStuff["From_y"][i]
            cc = ccvalue
            subject = mergedStuff["Subject"][i]
            draft(fromaddr, toaddr,messagebody, cc, subject)


