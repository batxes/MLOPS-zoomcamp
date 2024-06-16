#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip freeze | grep scikit-learn')


# In[2]:


get_ipython().system('python -V')


# In[3]:


import pickle
import pandas as pd


# In[6]:


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[7]:


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[8]:


df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet')


# In[9]:


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# In[14]:


#Q1:
df_results = pd.DataFrame()
df_results["predicted_duration"] = y_pred
print(df_results.std())


# In[16]:


year = 2023
month = 3
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


# In[17]:


df_results['ride_id'] = df['ride_id']


# In[20]:


df_results.to_parquet(
    f'pred_taxi_{year}_{month}',
    engine='pyarrow',
    compression=None,
    index=False
)


# In[21]:


df_results

# Q2: 66Mb.


# In[ ]:




