import re
import csv
import nltk
import en_core_web_sm
from nltk.corpus import stopwords
from values import *
stop = stopwords.words('english')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def getname(x):
    nlp = en_core_web_sm.load()
    doc = nlp(x)
    for X in doc.ents:
        if X.label_ == 'GPE' or X.label_ == 'PERSON':
            if X.text != yourname:
                return X.text


def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]


def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)


def connect(x):
    present = re.search("call |talk |reach |speak |contact |hear", x)
    date = getdate(x)
    if present:
        if date == 1:
            # mark date
            number = extract_phone_numbers(x)
            email = extract_email_addresses(x)
            name = getname(x)
            return number, email, name, date
        elif date == 2:
            # send calender
            number = extract_phone_numbers(x)
            email = extract_email_addresses(x)
            name = getname(x)
            return number, email, name, date
        elif date == 3:
            # send calender
            number = extract_phone_numbers(x)
            email = extract_email_addresses(x)
            name = getname(x)
            return number, email, name, date

    else:
        return False


def detail(x):
    present = re.search(
        "share ((detail|details)|write up){0}|((detail|detials)|write up){1}|brief (detail|write up)|demo", x)
    if present:
        return "share details"
    else:
        return False


def thirdperson(x):
    number = extract_phone_numbers(x)
    email = extract_email_addresses(x)
    name = getname(x)
    checkcc = re.search(" cc| CC", x)
    if name:
        if checkcc:
            return 1, name
        else:
            return 2, name
    else:
        return False


def getdate(x):
    present = re.search("today |tomorrow ", x)
    if present:
        time = re.search("(1[0-2]|0?[1-9]) ([AaPp][Mm])", x)
        if time:
            return 1
        else:
            return 2
    else:
        return 3

