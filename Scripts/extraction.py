#### RUN API EXTRACTION

import pandas as pd
import pandas.io.sql as sql
import pymysql
import xlwt
import sqlalchemy
import time
import civitatisAPI as civi
import requests
import json
import thefuzz


from requests.auth import HTTPBasicAuth

from sqlalchemy import create_engine
from pymysql import*
from datetime import date
from thefuzz import process

usr = 'bederapp'
pss ='w5OWhwNPL1tU'
lnag = 'en'
session = civi.Civitatis(username=usr,password=pss)
today = date.today()
d1 = today.strftime("%d_%m_%Y")


civitatis_countries = session.get_countries('en')
civitatis_countries_df = pd.DataFrame(civitatis_countries)

civitatis_countries_df.to_csv(f'C:\\Users\\beder\Desktop\Data 2022\Projects\CIVITATIS-IMPLEMENTATION2022\Outputs\Civitatis Exctraction\civitatis_countries{d1}.csv',index=False)

countries_dic = {}
for entry in civitatis_countries:
    countries_dic[entry['name']]=entry['id']


all_destinations_df =  pd.DataFrame(session.get_destinations('en'))

all_destinations_df.to_csv(f'C:\\Users\\beder\Desktop\Data 2022\Projects\CIVITATIS-IMPLEMENTATION2022\Outputs\Civitatis Exctraction\\all_destinations{d1}.csv',index=False)

acti_frames= []
for i, acti_id  in enumerate(all_destinations_df['id']):

    print(acti_id,i,len(all_destinations_df['id']),flush=True)
    acti_frames.append(pd.DataFrame(session.get_destination_activities(acti_id,'en')))

print('activities done')
all_activities = pd.concat(acti_frames)

longitude = []
latitude = []
for act in all_activities['address']:
    longitude.append(act['longitude'])
    latitude.append(act['latitude'])

all_activities['longitude'] =  longitude
all_activities['latitude'] =  latitude
all_activities.to_csv(f'C:\\Users\\beder\Desktop\Data 2022\Projects\CIVITATIS-IMPLEMENTATION2022\Outputs\Civitatis Exctraction\\all_activities{d1}.csv',index=False)


#MAPPING
user= 'beder'
password="DEjUYJjxfRSvab3T"
host="server.digizonelabs.com"
databases_schema = []

con=connect(user="beder",password="DEjUYJjxfRSvab3T",host="server.digizonelabs.com",database="beder_appprod")

countries=sql.read_sql('select * from beder_appprod.countries',con)
regions=sql.read_sql('select * from beder_appprod.regions',con)
provinces=sql.read_sql('select * from beder_appprod.provinces',con)
cities=sql.read_sql('select * from beder_appprod.cities',con)


countries =  countries[['country_id', 'google_id', 'english_name',
       'spanish_name']]


civitatis_countries = civitatis_countries_df['name'].unique()
countries_col = countries['english_name'].unique()
dic_replace = {}
for country in civitatis_countries:
    matches = process.extractOne(country, countries_col)
    if  90 <= matches[1] <100:
        dic_replace[country] = matches[0]

sant_bart = {'San Bartolomé':'Saint Barthélemy'}
dic_replace.update(sant_bart)
civitatis_countries_df['name'] = civitatis_countries_df['name'].replace(dic_replace, regex=True)


initial_merge = pd.merge(countries,civitatis_countries_df,how='left', left_on='english_name',right_on='name')
completed = initial_merge[initial_merge['name'].notna()]
completed.sample(10)

completed_dic = dict(zip(completed['country_id'],completed['id']))

manual_match = {18.0:148.0,
    20.0:180.0,
    45.0:24.0,
    51.0:180.0,
    52.0:180.0,
    53.0:180.0,
    90.0:276.0,
    105.0: 164.0,
    152.0:126.0,
    165.0:54.0,
    173.0:205.0,
    219.0: 167.0,
    221.0:201.0}

completed_dic.update(manual_match)
completed_df = pd.DataFrame.from_dict(completed_dic,orient='index')
completed_df = completed_df.reset_index()


countries_mapped= pd.merge(countries,completed_df, how = 'left', left_on='country_id',right_on='index')
countries_mapped.drop(['index'],axis= 1)
countries_mapped.rename(columns = {0:'id'}, inplace = True)
countries_mapped= countries_mapped.drop(['index'],axis= 1)

countries_merged = pd.merge(countries_mapped,civitatis_countries_df,how='left', on ='id')
countries_merged.to_csv(f'C:\\Users\\beder\Desktop\Data 2022\Projects\Activities Implementation\Outputs\Civitatis Exctraction\civitatis_countries_mapped.csv',index=False)