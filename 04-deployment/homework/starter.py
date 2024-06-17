#!/usr/bin/env python
# coding: utf-8

import os
import numpy
import sys
import pickle
import pandas as pd
print (numpy.version.version)


categorical = ['PULocationID', 'DOLocationID']

def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv,model

def read_data(filename):
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def prediction(year,month):
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')
    dv, model = load_model()
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    df_results = pd.DataFrame()
    df_results["predicted_duration"] = y_pred
    return df_results

def run():
    year = int(sys.argv[1]) #2023
    month = int(sys.argv[2]) #4
    df = prediction(year,month)
    # Q5 and Q6
    print(df.mean())
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_results = pd.DataFrame()
    df_results['ride_id'] = df['ride_id']
    df_results.to_parquet(
        f'pred_taxi_{year}_{month}',
        engine='pyarrow',
        compression=None,
        index=False
    )
    print (df_results)

if __name__ == "__main__":
    run()


