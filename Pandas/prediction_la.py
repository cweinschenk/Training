# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import numpy as np

incident_type = 'inc_type'
fire_spread = 'fire_sprd'
num_civ_injs = 'civilian_casualties'
num_ff_injs = 'firefighter_casualties'
aid_type_field = 'aidtype'
struc_type_field = 'struc_type'
inc_date_field = 'inc_date'
inc_date_format = '%Y%m%d'

data = pd.read_csv('us-ca-la_city-building_fires_2014_2015.csv',dtype={ 'aidtype':str,'struc_type':str,'inc_type': str,}) # read in city data
residential_structure_fires = data.loc[((data[aid_type_field] != '3') & (data[aid_type_field] != '4'))][(
                          (((data[incident_type]=='111')   | (data[incident_type]=='120')   | 
                             (data[incident_type]=='121')  | (data[incident_type]=='122')   | 
                             (data[incident_type]=='123')) & ((data[struc_type_field]=='1')  | 
                             (data[struc_type_field]=='2')))| (((data[incident_type]=='113') | 
                             (data[incident_type]=='114')  | (data[incident_type]=='115')   | 
                             (data[incident_type]=='116')  | (data[incident_type]=='117')   | 
                             (data[incident_type]=='118')) & ((data[struc_type_field]=='1')  | 
                             (data[struc_type_field]=='2')  | (data[struc_type_field]==''))))].copy()

residential_structure_fires['year']=pd.to_datetime(residential_structure_fires[inc_date_field], format=inc_date_format).dt.year
residential_structure_fires = residential_structure_fires[residential_structure_fires['year']==2015]
residential_structure_fires[incident_type] = residential_structure_fires[incident_type].replace('[a-zA-Z]$','', regex=True)
residential_structure_fires[fire_spread] = residential_structure_fires[fire_spread].replace('[a-zA-Z]','', regex=True)
residential_structure_fires[fire_spread] = residential_structure_fires[fire_spread].replace(np.nan, 0).astype(int)

causualties = residential_structure_fires.fillna(0)[num_civ_injs] + residential_structure_fires.fillna(0)[num_ff_injs]
print (sum(causualties), "actual casualties; 73 predicted")
firespread_incidents = residential_structure_fires[residential_structure_fires[fire_spread]]
print (len(firespread_incidents), "actual total firespread incidents; 2879 predicted")

