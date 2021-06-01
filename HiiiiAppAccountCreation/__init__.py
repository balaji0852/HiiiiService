import logging
import os
import azure.functions as func
import json
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:

    #getting the data required for account creation task
    data = req.get_json()

    #getting values of application settings 
    server = os.environ['Server']
    database =  os.environ["database"]
    username = os.environ["admin"]
    password = os.environ["password"]
    driver= '{ODBC Driver 17 for SQL Server}'

    #preparing the query string with json payload
    query = "insert into HyeAuthentication values('{}','{}','{}','{}','{}',{},{},{});".format(data.get('authid'),
    data.get('name'),data.get('phone'),data.get('email'),data.get('gender'),data.get('bicycle'),data.get('bike'),data.get('car'))


    try:
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return func.HttpResponse(json.dumps({"status":200}))

    except:
        return func.HttpResponse(json.dumps({"status":500}))

    
