import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import time
import boto3
from urllib.parse import urlparse
import datetime


st.title('ACME CRM Dashboard')
