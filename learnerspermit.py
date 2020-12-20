import requests
import json
import os
import time 

locations = {
    "Queens - College Point": "fb052d6eae67926d8d5449d7317c8528e1e3d02b19441ead85f3150915e2abbe",
    "Queens - Jamaca": "d0099bebf8e51979019b5e45b2c7dfeab9830f0213a4da0cfd569ec145eb07a9",
    "Queens college": "887df9bcd65c813a07ac3ae5e818d4faec1aa02bb467ea5cb2e1e2e878bfa32a",
    "lower manhattan": "8bcc5ca5cad16666ba6f5dd43d15241e172bd511f7e8d6f2e1caa2380b66776a",
    "midtown manhattan": "0ea16b72515a86e0cc00d186b249b0ebc61ed10b5289394af9b0cab8de5dafda",
    "brooklyn - atlantic av": "c92d2048b00326a0d9452e478db504ce41ec8f67f8e008034295cbf85cf902df"
}

service_id = "10226f4de0f460aa67bb735db97f9eb434b8ac2a144e40a20ff1e1848ffbeae7" # service id for learners permit

site_url = "https://nysdmvqw.us.qmatic.cloud/naoa/index.jsp"

def check():
    for location in locations:
        dates = json.loads(requests.get(f"https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/{locations[location]}/services/{service_id}/dates?_=1608422256259").content)
        print(dates)
        if len(dates) > 0:
            #os.system(f"terminal-notifier -title 'New Permit Test Dates' -message 'Register now at {location}'  -open ${site_url}")
            for obj in dates:
                date = obj["date"]
                times = json.loads(requests.get(f"https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/{locations[location]}/services/{service_id}/dates/{date}/times?_=1608422256273").content)
                if len(times) > 0:
                    time = times[-1]["time"] # chooses the latest time
                    req_json = {
                        'appointment': {
                            'customers': [],
                            'resources': []
                        },
                    }
                    reservation = json.loads(requests.post(f"https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/branches/{locations[location]}/services/{service_id}/dates/{date}/times/{time}/reserve", json=req_json).content)
                    res_id = reservation['publicId']
                    me_json = {
                        'appointmentReference': '',
                        'customer': { 
                            'dateOfBirth': "", # enter your date of birth in year-month-day ie. 2000-12-31
                            'email': '', #enter your email
                            'externalId': '', # leave blank
                            'firstName': "Sofiane", #first name
                            'lastName': "Larbi", #first name
                            'phone': '' # enter phone in ###-###-#### format
                        },
                        'languageCode': 'en-US',
                        'notes': '',
                        'notificationType': '',
                        'title': ''
                    }
                    confirmation = json.loads(requests.post(f"https://nysdmvqw.us.qmatic.cloud/qwebbook/rest/schedule/appointments/{res_id}/confirm", json=me_json).content)
                    #you have to do 'brew install terminal-notifier' for this to work in your terminal
                    os.system(f"terminal-notifier -title 'New Permit Test Appointment' -message 'Registered successfully at {location}'  -open ${site_url}")
                    print(confirmation)
                    exit()


if __name__ == '__main__':
    while True:
        check()
        time.sleep(60)