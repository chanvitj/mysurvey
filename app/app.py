from pywebio import start_server
from pywebio.input import *
#from pywebio.input import input, NUMBER, TEXT, input_group, actions, checkbox
from pywebio.output import put_html, popup, put_buttons, close_popup, put_text, put_image
import pymongo
import datetime
import re
import os

mongoDBString = os.environ['MONGODB_STRING']
mongbDBName = os.environ['MONGODB_DBNAME']
mongoDBCollection =os.environ['MONGODB_COLLECTIONNAME']

def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return 
    else:
        return "Invalid Email"

def checkDate(date):
    if (date==''):
        return "Invalid date"
    else:
        return
    
def validateMobile(value):
    """ Raise a ValidationError if the value looks like a mobile telephone number.
    """
    validatePhoneNumberPattern = '0[0-9]{9}$'
    r=re.match(validatePhoneNumberPattern, value)
    if (not r):
        return "Phone is not correct"
    else:
        return

def recordToDB(info):
    client = pymongo.MongoClient(mongoDBString)
    db = client[mongbDBName]
    col = db[mongoDBCollection]

    if info['action'] == "Submit":
        x = datetime.datetime.now()
        d = x.strftime("%Y-%m-%d")
        t = x.strftime("%H:%M:%S")

        mydict = {
            "Date": d, 
            "Time": t, 
            "name": info['name'].upper(), 
            "emailAddress": info['emailAddress'], 
            "mobileNumber": info['mobileNumber'], 
            "company": info['company'],
            "jobTitle": info['jobTitle'],
            "callBackForProductInformation": info['callBackForProductInformation'],
            "attendNextSeminar": info['attendNextSeminar'],
            "planToMigrate": info['planToMigrate'],
            "callBackHowToSecureCloud": info['callBackHowToSecureCloud']
        }
        r = col.insert_one(mydict)
        print(r.inserted_id)

def main():
    img = open("./fortinet-logo.png", "rb").read()
    put_image(img, width='30%')

    info = input_group("Public Cloud Training - After Training Survey", [
        input("Name", type=TEXT, name='name'),
        input("Email Address*", type=TEXT, validate=checkEmail, name='emailAddress'),
        input("Mobile Number*", type=TEXT, validate=validateMobile, name='mobileNumber'),
        input("Company*", type=TEXT, name='company'),
        input("Job Title*", type=TEXT, name='jobTitle'),
        checkbox("ท่านต้องการให้ติดต่อกลับเพื่อแจ้งข้อมูลที่เกี่ยวข้องกับผลิตภัณฑ์ดังต่อไปนี้", 
            # name='nextTrainings', options=[
            name='callBackForProductInformation', options=[
                "FortiGate",
                "FortiWeb",
                "FortiADC",
                "ไม่ต้องการให้ติดต่อกลับเพื่อแจ้งข้อมูลผลิตภัณฑ์"
            ]
        ),
        radio("ท่านต้องการให้แจ้งข้อมูลงานสัมมนาครั้งถัดไปหรือไม่",
            name="attendNextSeminar",
            options=[ "yes", "no" ],
            required=True
        ),
        radio("บริษัทของท่านกำลังวางแผนนำระบบหรือ application หรือฐานข้อมูลขึ้น Cloud หรือไม่",
            name="planToMigrate",
            options=[ "yes", "no" ],
            required=True 
        ),
        radio("ท่านต้องการให้ทาง Fortinet ติดต่อกลับเพื่อให้ข้อมูลวิธีการรักษาความปลอดภัยบน Cloud หรือไม่",
            name="callBackHowToSecureCloud",
            options=[ "yes", "no" ],
            required=True 
        ),
        actions('', [
            {'label': 'Submit', 'value': 'Submit'},
            {'label': 'Cancel', 'value': 'Cancel', 'color': 'warning'},
        ], name='action')
    ])

    print(info)
    recordToDB(info)
    put_text('Survey is submitted.')

if __name__ == '__main__':
    start_server(main, debug=True, port=8081)
