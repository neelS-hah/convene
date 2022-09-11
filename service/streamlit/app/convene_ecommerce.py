from typing import final
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import time
import boto3
from urllib.parse import urlparse
import datetime
from streamlit_imagegrid import streamlit_imagegrid
import requests

# def convene_run():
s3 = boto3.client('s3')

with st.sidebar:
    st.title('Acme Inc.')
    st.write('Account')
    st.write('Settings')
    st.write('Help')
    st.write('Logout')


st.title('Convene E-commerce Dashboard')
# BUCKET = "acme-convene-demo"
with st.container():
     tab1, tab2 = st.tabs(["Upload File", "Input File S3 Path"])
     generated = False
     final_url = None
     with tab1:
          uploaded_file = st.file_uploader("Choose a file")
          if uploaded_file is not None:
               # Can be used wherever a "file-like" object is accepted:
               dataframe = pd.read_csv(uploaded_file)
               dataframe.to_csv('local_file.csv', index=False)

               my_expander = st.expander(label='Preview Data')
               with my_expander:
                    st.write(dataframe)
               
               schema = pd.DataFrame(list(dataframe))
               # st.subheader('Select Values: ')
               values_selector = st.expander(label='Select Values')
               with values_selector:
                    # st.write(dataframe)
                    for index,elem in schema.iterrows():
                         datatype = type(elem.iloc[0])
                         st.checkbox(elem.iloc[0] + '  '+ f'  {datatype}', value = True)
               #   st.write("\t\t"+str(datatype))
                    
               st.write('\n')
               bucket =st.text_input('Enter S3 Bucket Name: ', placeholder='my-bucket', value='acme-convene-demo')
               if st.button('Submit ', on_click=None):
                    with st.spinner(text="In progress..."):
                         time.sleep(3)
                         st.success('Done!')
                    current_date = datetime.datetime.now()
                    folder_time = current_date.strftime("%Y-%m-%d")
                    file_time = current_date.strftime("%Y-%m-%d-%H-%M-%S")
                    result_path = f"results/{folder_time}/{file_time}_generated_product_catalog.csv"
                    region = "us-east-2"
                    s3.upload_file("final_product_catalog.csv",bucket,result_path)
                    url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket, region,result_path)
                    generated = True
                    st.markdown("""---""")
                    col1, col2, col3 = st.columns(3)
                    urlData = requests.get(url).content
                    result_data = pd.read_csv(StringIO(urlData.decode('utf-8')))
                    col1.metric("Records Processed", len(dataframe))
                    col2.metric("Attributes", '12,657,400')
                    col3.metric("Deduped Records", len(result_data), f"{int(100*(1-(len(result_data)/len(dataframe))))}% deduped")
                    st.write(f"URL: {url}")



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
                         st.subheader("URL: ")
                         st.write(url)
                         generated = True


with st.container():
     if generated:
          # st.markdown("""---""")
          from PIL import Image
          st.subheader('Catalog Preview')
          col1, col2, col3 = st.columns(3)
          with col1:
               image = Image.open('images/1.jpeg')
               st.image(image, caption='Patagonia Shirt', use_column_width=True)
          with col2:
               image = Image.open('images/2.jpeg')
               st.image(image, caption='Patagonia Jacket', use_column_width=True)
          with col3:
               image = Image.open('images/3.jpeg')
               st.image(image, caption='Patagonia Sweatshirt', use_column_width=True)    

st.markdown("""---""")




