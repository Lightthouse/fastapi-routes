import json
import os.path

from time import ctime
from typing import Optional, List
from fastapi import FastAPI, Request, Form, Query, Body, Depends, Header, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.classes.secret_one_application import SecretOneApplication
from app.classes.secret_subscription import SecretSubscription
from app.classes.response_model import ResponseModel


app = FastAPI()


@app.get("/arguments_1/")
def get_one(first_name: str, second_name: str, third_name: str):
    return {"first_name": first_name, "second_name": second_name, "third_name": third_name}


@app.get("/arguments_2/")
def get_second(first_name: str, second_name: str, third_name: str, nick_name: Optional[str] = Query(None)):
    return {"first_name": first_name, "second_name": second_name, "third_name": third_name, "nick_name": nick_name}


@app.get("/arguments_3/")
def get_third(name: str, nick_name: Optional[str] = Query("admin"), current_time=ctime()):
    return {"name": name, "nick_name": nick_name, "current_time": current_time}


# json
@app.post("/json/")
def json_data(applications: List[SecretOneApplication], subscription: SecretSubscription, token: str = Body(...)):
    return {"app": applications, "sub": subscription, "token": token}


# form-data
@app.post("/form/")
def form_data(first_name: str = Form(...), second_name: str = Form(...), third_name: str = Form(...)):
    return {"first_name": first_name, "second_name": second_name, "third_name": third_name}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/upload_file/")
async def create_upload_file(file: UploadFile = File(...)):
    with open('app/public/newFile.txt', 'wb') as f:
        [f.write(chunk) for chunk in iter(lambda: file.file.read(10000), b'')]
    return {"filename": file.filename}


# headers
@app.post("/headers/")
def header(x_api_key: str = Header(...), referer: Optional[str] = Header(None)):
    with open('app/settings/headers.json', 'r') as j:
        json_value = json.load(j)

    return (json_value['referer'] == referer) and (x_api_key.isdigit())


# request
@app.post("/request/")
async def request(rqst: Request):
    json_body = await rqst.json()
    return {"body": json_body, "query": rqst.query_params, "headers": rqst.headers, "form": rqst.form}


# response
@app.post("/response/", response_model=ResponseModel)
def json_answer(resp: ResponseModel):
    return resp


@app.get("/response_file/{file_name}")
def file_answer(file_name: str):
    some_file_path = f'app/public/{file_name}.jpg'
    if not os.path.isfile(some_file_path):
        rp_m = ResponseModel()
        rp_m.is_complete = False
        rp_m.error = 'there are no files with that name'
        return rp_m
    return FileResponse(some_file_path)


# exceptions
@app.get("/error/{status_code}")
def exc(status_code: int):
    raise HTTPException(status_code=status_code, detail="error lives here")


# dependencies
def check_file(referer: Optional[str] = Header(...)):
    with open('app/settings/headers.json', 'r') as j:
        json_value = json.load(j)
    if json_value['referer'] != referer:
        raise HTTPException(status_code=400, detail="text different from file")


@app.post("/dep/", dependencies=[Depends(check_file)])
def dep():
    return True
