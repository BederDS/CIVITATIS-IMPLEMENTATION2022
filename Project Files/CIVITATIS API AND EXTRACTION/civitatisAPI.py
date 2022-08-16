
import requests
import json
import pandas as pd

from requests.auth import HTTPBasicAuth
from IPython.display import clear_output



class Civitatis():
    def __init__(self, username,password):
        self.username = username
        self.password = password
        authentication = {'username':username,'password':password}

    ## Initialize a Session with session requests object
        session = requests.Session()
        response  = session.post('https://api.civitatis.com/v2/auth',json=authentication)
        if (response.status_code == 200):
            self.token = response.json()['token']
        else:
            print(response.status_code)

        self.myheader = {'Authorization': f'Bearer {self.token}'}
        pass

    def get_countries(self,language):
        r = requests.get('https://api.civitatis.com/v2/countries',params={'lang':language},headers=self.myheader)
        return r.json()
    
    def get_country_details(self,country_id,language):
        r = requests.get(f'https://api.civitatis.com/v2/countries/{country_id}',params={'lang':language},\
            headers=self.myheader)
        return r.json()

    def get_country_destinations(self,country_id,language):
        r = requests.get(f'https://api.civitatis.com/v2/countries/{country_id}/destinations',params={'lang':language},\
            headers=self.myheader)
        if (r.status_code ==204):
            return ('No destinations')
        elif (r.status_code ==200):
            return r.json()

    def get_destinations(self,language):
        r = requests.get('https://api.civitatis.com/v2/destinations',params={'lang':language},headers=self.myheader)
        return r.json()  

    def get_destination_details(self,destination_id,language):
        r = requests.get(f'https://api.civitatis.com/v2/destinations/{destination_id}',params={'lang':language},\
            headers=self.myheader)
        return r.json()
    
    def get_destination_activities(self,destination_id,language):
        r = requests.get(f'https://api.civitatis.com/v2/destinations/{destination_id}/activities',params={'lang':language},\
            headers=self.myheader)
        string_val = r.text
        before, sep, after = string_val.partition('[')
        string_final = sep+after
        return json.loads(string_final)

    def activity_details(self,activity_id):
        r = requests.get(f'https://api.civitatis.com/v2/activities/{activity_id}', headers=self.myheader)
        return r.json()
    
    def activity_checkout(self,activity_id):
        r = requests.get(f'https://api.civitatis.com/v2/activities/{activity_id}/checkoutData', headers=self.myheader)
        return r.json()

    def closeby_act(self,lat,long,distance):
        r = requests.post('https://api.civitatis.com/v2/findByCoord',json={'lat':lat,'long':long,'distance':distance},headers=self.myheader)
        return r.json()
    
    def typologies(self,language):
        r = requests.get(f'https://api.civitatis.com/v2/typologies',params={'lang':language},\
            headers=self.myheader)
        return r.json()

