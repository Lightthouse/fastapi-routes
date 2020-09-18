import json
import os.path

from time import ctime
from typing import Optional, List
from fastapi import FastAPI, Request, Form, Query, Body, Depends, Header, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from classes import ResponseModel
from classes import SecretOneApplication
from classes import SecretTokenCache
from classes import SecretSubscription


app = FastAPI(title='fast-api routes',
              description='Сборник стандартных роутов fastapi')


@app.get("/arguments_1/", name='query 3 обязательных параметра')
def get_one(first_name: str, second_name: str, middle: str):
    """
    <pre>
    Получение 3 обязательных параметра из query строки.
    Параметры запроса:
        second_name [string] - фамилия.
        first_name [string] - имя.
        middle_name [string] - отчество.
    </pre>
    """
    return {"second_name": second_name, "first_name": first_name, "middle_name": middle}


@app.get("/arguments_2/", name='query 3 обязательных и 1 необязательный параметр')
def get_second(first_name: str, second_name: str, middle_name: str, nick_name: Optional[str] = Query(None)):
    """
    <pre>
    Получение 3 обязательных параметра и 1 необязательного из query строки.
    Параметры запроса:
        second_name [string] - фамилия.
        first_name [string] - имя.
        middle_name [string] - отчество.
        nick_name [string] - кличка.
    </pre>
    """
    return {"first_name": first_name, "second_name": second_name, "middle_name": middle_name, "nick_name": nick_name}


@app.get("/arguments_3/", name='query 1 обязательный параметр, 1 необязательный и 1 по умолчанию')
def get_third(name: str, nick_name: Optional[str] = Query("admin"), current_time=ctime()):
    """
    <pre>
    Получение 1 обязательного параметра, 1 необязательного и 1 по умолчанию из query строки.
    Параметры запроса:
        name [string] - имя.
        nick_name [string] - кличка.
        current_time [string] - время.
    </pre>
    """
    return {"name": name, "nick_name": nick_name, "current_time": current_time}


# json
@app.post("/json/", name='keyVault secret')
def json_data(applications: List[SecretOneApplication], subscription: SecretSubscription, token: str = Body(...)):
    """
    <pre>
    Получение секрета keyVault в формате json.
    Параметры запроса:
        applications [list] - список сервисов.
            type [str] - тип сервиса.
            subdomain [str] - субдомейн клиента.
            client_id [str] - id клиента из инетграции.
            client_secret [str] - секрет интеграции.
            account_id [int] - id аккаунта.
            account_name [str] - название аккаунта.
            token_cache [object]:
                token_type [str] - тип токена.
                expires_in [int] - время жизни токена.
                access_token [str] - токена доступа.
                refresh_token [str] - токен обновления токенов.
                expires_at [int] - конец жизни токена.
        subscription [string]:
            enabled [bool] - активна ли подписка.
            date_start [int] - дата начала подписки.
            date_end [int] - дата конца подписка.
            generations_count [int] - количество генераций.
            generations_limit [int] - лимит генераций.
        token [string] - авторизационный токен.
    </pre>
    """
    return {"app": applications, "sub": subscription, "token": token}


# form-data
@app.post("/form/", name='3 обязательных параметра')
def form_data(first_name: str = Form(...), second_name: str = Form(...), middle_name: str = Form(...)):
    """
    <pre>
    Получение 3 обязательных параметра из form-data.
    Параметры запроса:
        second_name [string] - фамилия.
        first_name [string] - имя.
        middle_name [string] - отчество.
    </pre>
    """
    return {"second_name": second_name,  "first_name": first_name, "middle_name": middle_name}


@app.post("/files/", name='Размер файла')
async def create_file(file: bytes = File(...)):
    """
    <pre>
    Загрузка файла и вычисление его размера.
    Параметры запроса:
        file [bytes] - загружаемый файл.
    </pre>
    """
    return {"file_size": len(file)}


@app.post("/upload_file/", name='Загрузка файла')
async def create_upload_file(file: UploadFile = File(...)):
    """
    <pre>
    Загрузка файла и сохранение его в папку.
    Параметры запроса:
        file [bytes] - загружаемый файл.
    </pre>
    """
    with open('public/newFile.txt', 'wb') as f:
        [f.write(chunk) for chunk in iter(lambda: file.file.read(10000), b'')]
    return {"filename": file.filename}


# headers
@app.post("/headers/", name='Заголовки')
def header(x_api_key: str = Header(...), refer: str = Header(None)):
    """
    <pre>
    Получение 1 обязательного параметра и 1 необязательного из headers.
    Параметры запроса:
        x_api_key [str] - токен авторизации.
        referer [str] - строка с информацией.
    </pre>
    """
    with open('settings/headers.json', 'r') as j:
        json_value = json.load(j)

    return (json_value['referer'] == refer) and (x_api_key.isdigit())


# request
@app.post("/request/", name='Тело запроса')
async def request(rqst: Request):
    """
    <pre>
    Получение полной информации о входящем запросе.
    Параметры запроса:
        rqst [Request] - входящий запрос.
    </pre>
    """
    json_body = await rqst.json()
    body_body = await rqst.body()
    return {"body": body_body, "query": rqst.query_params, "headers": rqst.headers, "form": rqst.form, "json_body": json_body}


# response
@app.post("/response/", response_model=ResponseModel, name='Модель ответа')
def json_answer(resp: ResponseModel):
    """
    <pre>
    Создание модели ответа для документации, на основе входящих данных.
    Параметры запроса:
        resp [ResponseModel] - входящий запрос, соответствующий модели ответа.
    </pre>
    """
    return resp


@app.get("/response_file/{file_name}", name='Скачивание файла')
def file_answer(file_name: str):
    """
    <pre>
    Загрузка файла из локальной папки по его имени.
    Параметры запроса:
        file_name [str] - имя файла.
    </pre>
    """
    some_file_path = f'app/public/{file_name}.jpg'
    if not os.path.isfile(some_file_path):
        rp_m = ResponseModel()
        rp_m.is_complete = False
        rp_m.error = 'there are no files with that name'
        return rp_m
    return FileResponse(some_file_path)


# exceptions
@app.get("/error/{status_code}", name='Код ошибки')
def exc(status_code: int):
    """
    <pre>
    Получение ошибки запроса.
    Параметры запроса:
        status_code [int] - код возвращаемой ошибки.
    </pre>
    """
    raise HTTPException(status_code=status_code, detail="error lives here")


# dependencies
def check_file(referer: Optional[str] = Header(...)):
    with open('settings/headers.json', 'r') as j:
        json_value = json.load(j)
    if json_value['referer'] != referer:
        raise HTTPException(status_code=400, detail="text different from file")


@app.post("/dep/", dependencies=[Depends(check_file)], name='Зависимости с валидацией')
def dep():
    """
    <pre>
    Выполнение проверки входящего заголовка со значением в файле до того, как запустится роут.
    Параметры запроса:
        referer [str] - сообщение для проверки.
    </pre>
    """
    return True
