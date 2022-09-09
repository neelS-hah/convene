import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import time
import boto3
from urllib.parse import urlparse
import datetime


# def convene_run():
s3 = boto3.client('s3')


st.title('ACME Market Convene Dashboard')

# BUCKET = "acme-convene-demo"
tab1, tab2 = st.tabs(["Upload File", "Input File S3 Path"])

with tab1:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        dataframe.to_csv('local_file.csv', index=False)
        st.write(dataframe)
        
        schema = pd.DataFrame(list(dataframe))
        st.subheader('Select Values: ')
        for index,elem in schema.iterrows():
          datatype = type(elem.iloc[0])
          st.checkbox(elem.iloc[0] + '  '+ f'  {datatype}', value = True)
        #   st.write("\t\t"+str(datatype))
          
        st.write('\n')
        bucket =st.text_input('Enter S3 Bucket Name: ', placeholder='my-bucket')
        if st.button('Submit ', on_click=None):
            current_date = datetime.datetime.now()
            folder_time = current_date.strftime("%Y-%m-%d")
            file_time = current_date.strftime("%Y-%m-%d-%H-%M-%S")
            result_path = f"results/{folder_time}/{file_time}_generated_product_catalog.csv"
            region = "us-east-2"
            s3.upload_file("local_file.csv",bucket,result_path)
            url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket, region,result_path)
            st.write(url)


with tab2:
    s3_path = st.text_input('S3 Path', placeholder='s3://...')
    if st.button('Submit', on_click=None):
          with st.spinner(text="In progress..."):
               time.sleep(5)
               st.success('Done!')
    
          if s3_path != "":
               s3_url_parsed = urlparse(s3_path)
               st.write(s3_url_parsed)

               if s3_url_parsed.scheme != "s3":
                    st.write("Invalid s3 path")

               current_date = datetime.datetime.now()
               folder_time = current_date.strftime("%Y-%m-%d")
               file_time = current_date.strftime("%Y-%m-%d-%H-%M-%S")

                
               bucket = s3_url_parsed.netloc
               key = s3_url_parsed.path.lstrip('/')
               result_path = f"results/{folder_time}/{file_time}_generated_product_catalog.csv"
               s3.download_file(bucket, key, 'local_file.csv')
               region = "us-east-2"
               s3.upload_file("local_file.csv",bucket,result_path)
               url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket, region,result_path)
               st.write(url)
            #    return {"result_path": result_path, "url": url}


    





