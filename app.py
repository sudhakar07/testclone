import streamlit as st
import numpy as np
from math import sqrt
import pandas as pd

print("Awesome")

#st.title("Welcome To Streamlit DS HeroKu App")



st.title("Coronavirus (COVID-19) Dashboard")


confirmed = pd.read_csv("time_series_covid19_confirmed_global.csv")
#url = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
death = pd.read_csv("time_series_covid19_deaths_global.csv")
#url = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
recover = pd.read_csv("time_series_covid19_recovered_global.csv")

confirmed['Country/Region']= confirmed['Country/Region'].str.replace("Mainland China", "China")
confirmed['Country/Region']= confirmed['Country/Region'].str.replace("US", "Unites States")
death['Country/Region']= death['Country/Region'].str.replace("Mainland China", "China")
death['Country/Region']= death['Country/Region'].str.replace("US", "Unites States")
recover['Country/Region']= recover['Country/Region'].str.replace("Mainland China", "China")
recover['Country/Region']= recover['Country/Region'].str.replace("US", "Unites States")


population=pd.read_csv('population.csv', sep=',', encoding='latin1') 
confirmed=pd.merge(confirmed, population,how='left' ,on=['Province/State','Country/Region'])
death=pd.merge(death, population,how='left' ,on=['Province/State','Country/Region'])
recover=pd.merge(recover, population,how='left' ,on=['Province/State','Country/Region'])


confirmed['region']=confirmed['Country/Region'].map(str)+'_'+confirmed['Province/State'].map(str)
death['region']=death['Country/Region'].map(str)+'_'+death['Province/State'].map(str)
recover['region']=recover['Country/Region'].map(str)+'_'+recover['Province/State'].map(str)
print(confirmed.iloc[:5,:])


def create_ts(df):
  ts=df
  ts=ts.drop(['Province/State', 'Country/Region','Lat', 'Long',' Population '], axis=1)
  ts.set_index('region')
  ts=ts.T
  ts.columns=ts.loc['region']
  ts=ts.drop('region')
  ts=ts.fillna(0)
  ts=ts.reindex(sorted(ts.columns), axis=1)
  return (ts)

ts=create_ts(confirmed)
ts_d=create_ts(death)
ts_rec=create_ts(recover)

print("Test pyplot start")


print("Test pyplot start2")

p=ts
tra=ts.reindex(sorted(ts.columns), axis=1)
tra.to_csv('file1.csv') 

confirmed2 = pd.read_csv("file1.csv")
print(confirmed2['India_nan'])
print(confirmed2.iloc[:,0])
data = {'date':confirmed2.iloc[:,0], 'india':confirmed2['India_nan']} 
  
# Create DataFrame 
df_by_date = pd.DataFrame(data) 
#print(df_by_date);
#print(tra['India_nan'].value_counts().plot(kind='line',figsize=(20,10)))
#print(tra[tra=="India_nan"])
#tra.to_csv('file1.csv') 
#print(ts.groupby('India'))
#print(p.head)
#print(p.describe());

df_by_date1 = df_by_date.groupby(['date']).sum()
df_by_date1[['india']].plot(marker='*',kind='line',figsize=(10,4)).set_title(' Total Confirmed - India',fontdict={'fontsize': 22})
st.pyplot()

#df_by_date['cases_date'] = pd.to_datetime(df_by_date['date'])
#df_by_date['cases_date'].value_counts().plot(figsize=(10,5))

df_by_date2 = df_by_date.groupby(['date']).max()
#df_by_date2[['india']].plot(marker='*',figsize=(10,4)).set_title('Max No of Cases India',fontdict={'fontsize': 22})

df_by_date3 = df_by_date.groupby(['date']).min()
#df_by_date3[['india']].plot(marker='*',figsize=(10,4)).set_title('Min No of Cases India',fontdict={'fontsize': 22})

df_by_date4 = df_by_date.groupby(['date']).idxmax()
#df_by_date4[['india']].plot(marker='*',figsize=(10,4)).set_title('Date for Maximum Number Cases',fontdict={'fontsize': 22})



p=ts.reindex(ts.max().sort_values(ascending=False).index, axis=1)
#p.iloc[:,:1].plot(marker='*',figsize=(10,4)).set_title('Daily Total Confirmed - US',fontdict={'fontsize': 22})
p.iloc[:,2:10].plot(marker='*',figsize=(10,4)).set_title(' Total Confirmed - Major areas',fontdict={'fontsize': 22})
st.pyplot()

p_d=ts_d.reindex(ts.mean().sort_values(ascending=False).index, axis=1)
#p_d.iloc[:,:1].plot(marker='*',figsize=(10,4)).set_title('Daily Total Death - US',fontdict={'fontsize': 22})
p_d.iloc[:,2:10].plot(marker='*',figsize=(10,4)).set_title(' Total Death - Major areas',fontdict={'fontsize': 22})
st.pyplot()

p_r=ts_rec.reindex(ts.mean().sort_values(ascending=False).index, axis=1)
#p_r.iloc[:,:1].plot(marker='*',figsize=(10,4)).set_title('Daily Total Recoverd - US',fontdict={'fontsize': 22})
p_r.iloc[:,2:10].plot(marker='*',figsize=(10,4)).set_title(' Total Recoverd - Major areas',fontdict={'fontsize': 22})
st.pyplot()
