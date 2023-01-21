import sys
from MaltegoTransform import *
import requests

# Create a Maltego transform object
m = MaltegoTransform()

# Get the email address from the Maltego entity
email = m.getVar("email")

def check_email(email):
    # Make an API call to the HaveIBeenPwned API
    response = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}')
    if response.status_code == 200:
        breaches = response.json()
        for breach in breaches:
            # Add a new entity to the Maltego graph for each breach
            m.addEntity("maltego.Breach", breach["Name"])
        search_dehashed(email)
    else:
        m.addUIMessage("The email address has not been compromised.")

def search_dehashed(email):
    # Make an API call to the Dehashed API
    api_key = 'YOUR_API_KEY'
    response = requests.get(f'https://api.dehashed.com/search?query={email}&api_key={api_key}')
    if response.status_code == 200:
        data = response.json()
        if data.get('records'):
            for record in data['records']:
                # Add a new entity to the Maltego graph for each breach found in dehashed
                m.addEntity("maltego.Breach", record['breach'])
                # Add new entities for each object returned in the Dehashed API
                for key, value in record.items():
                    if key == 'email':
                        m.addEntity("maltego.EmailAddress", value)
                    elif key == 'username':
                        m.addEntity("maltego.Username", value)
                    elif key == 'password':
                        m.addEntity("maltego.Password", value)
                    elif key == 'phone':
                        m.addEntity("maltego.PhoneNumber", value)
                    elif key == 'address':
                        m.addEntity("maltego.Location", value)
    else:
        m.addUIMessage("Error: Unable to fetch data from Dehashed API.")

check_email(email)

# Return the Maltego graph to the user
m.returnOutput()
