import imaplib
from email.parser import BytesParser
from pprint import pprint
import email.header
import time
import json
from values import *

# Settings
username = username
password = password

# path to ouput file name (leave off the extention)
ouput_filename = 'all_emailsent'  # output of all data, note extension is on next variable
output_type = 'json'

imapAddress = 'imap.gmail.com'

column_names = ['n', 'From', 'To', 'Subject', 'Date', 'Received', 'Rfc822msgid', 'Size', 'uid', 'Attachments',
                'text/plain', 'text/html', ]

chunk = 100  # number emails to ask for at each fetch imap server
start = 0  # start from first message


# endAt = 1000

def f_recieved(s): return {'Rfc822msgid': f'Rfc822msgid:{s}'};  # just past this into gmail to find message


# specify header parts to save and any conversion functions on them
key_map = {'From': None, 'To': None, 'Subject': None, 'Date': None,
           'Received': None, 'Message-ID': f_recieved, }


def parse_parts(msg, key_map):
    ''' return {key:msg[header_key]} or {parse_fun(msg[header_key]) as instructed in keymap'''
    parts = {}
    for hkey in key_map:
        raw = msg[hkey]
        if raw:
            if isinstance(raw, email.header.Header): raw = str(raw)  # to fix non ascii parts
            f = key_map[hkey]
            if f:
                fparts = f(raw)
                for k in fparts: parts[k] = fparts[k]
            else:
                parts[hkey] = raw
    return parts


def decode_part(part, mime_type):  # decode a part from the correct char coding. This was tricky
    charset = part.get_content_charset()
    if part.get_content_type() == mime_type:
        part_str = part.get_payload(decode=1)
        if charset == None:  # this is when the coding is not in the email data
            charset = 'utf-8'  # assume utf-8 then
        try:
            return part_str.decode(charset, 'replace')  # and try with replacement
        except:
            print(f"** pos {pos} {parts['Rfc822msgid']}:Decode Error, {mime_type} part skipped")
            pprint(part_str)  # and print what caused the error
            print('----------')
            return ""  # no part if error
    return ""


def decode_email(msg_str, key_map):
    filenames = None
    p = BytesParser()
    message = p.parsebytes(msg_str)
    parts = parse_parts(message, key_map)
    parts['Size'] = len(msg_str)
    plain_body = ''
    html_body = ''
    for part in message.walk():

        plain_body += decode_part(part, 'text/plain')
        if len(plain_body) > 0:
            html_body = ""
        else:
            html_body += decode_part(part, 'text/html')

        fn = part.get_filename()
        if fn:
            if filenames == None: filenames = []
            filenames.append(fn)
    if filenames:
        parts['Attachments'] = filenames
    if len(plain_body) > 0:
        parts['text/plain'] = plain_body
    elif len(html_body) > 0:
        parts['text/html'] = html_body
    return parts


def store_json(file, recs):
    with open(file + '.json', 'w') as f:
        f.write(json.dumps(recs, sort_keys=True, indent=4))


def sentcheck():
    ms = imaplib.IMAP4_SSL(imapAddress)
    ms.login(username, password)
    if ms.state == "AUTH":
        print("logged in OK")
    else:
        print("login Failed")
        exit(1)

    ms.select('"[Gmail]/Sent Mail"')
    result, data = ms.search(None, 'UNSEEN')
    uids = data[0].split()
    n = len(uids)
    id = 0
    recs = []
    for num in uids:
        print("fetching ", id + 1, "out of ", n)
        resp, data = ms.fetch(num, '(RFC822)')
        for msg in (m[1] for m in data if isinstance(m, tuple)):
            parts = decode_email(msg, key_map)
            parts['uid'] = str(num)
            recs.append(parts)
        id = id + 1
    typ, data = ms.search(None, 'ALL')
    for num in data[0].split():
        ms.store(num, '+FLAGS', '\\Deleted')
    ms.expunge()
    ms.logout()

    if output_type == 'json':
        store_json(ouput_filename, recs)

    print('*** DONE ***')



