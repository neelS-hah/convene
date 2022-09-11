from distutils.command.upload import upload
import shutil
from tkinter import W
from fastapi import FastAPI, UploadFile
import boto3
import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional

app = FastAPI()

BUCKET = "acme-convene-demo"

class LOCTYPE(str, Enum):
    s3 = "s3"
    body = "body"

@app.get("/")
def read_root():
    return {"Welcome to Convene!"}

class ProcessParams(BaseModel):
    loc: LOCTYPE
    location_path: Optional[str] = None
    upload_file: Optional[UploadFile] = None

@app.post("/convene/process")
async def convene_process(params: ProcessParams):
    if params.loc != LOCTYPE.body and params.location_path is None:
        return {"error": "location_path must be specified for this location type"}
    if params.loc == LOCTYPE.body and params.upload_file is None:
        return {"error": "upload_file must be specified for this location type"}
    result_path = ""
    current_date = datetime.datetime.now()
    folder_time = current_date.strftime("%Y-%m-%d")
    file_time = current_date.strftime("%Y-%m-%d-%H-%M-%S")


    if params.loc == LOCTYPE.s3:
        s3 = boto3.client('s3')
        s3.download_file(BUCKET, params.location_path, 'local_file.csv')
        result_path = f"results/{folder_time}/{file_time}_generated_product_catalog.csv"
    
    elif params.loc == LOCTYPE.body:
        with open("local_file.csv", "wb") as buffer:
            shutil.copyfileobj(params.upload_file.file, buffer)
        result_path = f"results/{folder_time}/{file_time}_generated_product_catalog.csv"
    
    if len(result_path)== 0:
        return {"error": "no result path"}

    try:
        region = "us-east-2"
        s3.upload_file("final_product_catalog.csv",BUCKET,result_path)
        url = "https://%s.s3.%s.amazonaws.com/%s" % (BUCKET, region, result_path)
        return {"result_path": result_path, "url": url}
    except Exception as e:
        print(e)
        return {"error": "Failed to upload to s3 due to exception: " + str(e)}
