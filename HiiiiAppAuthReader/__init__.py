import logging
import json
import azure.functions as func
import pyodbc
import os


def main(req: func.HttpRequest) -> func.HttpResponse:

   
    #getting values of application settings 
    server = os.environ['Server']
    database =  os.environ["database"]
    username = os.environ["admin"]
    password = os.environ["password"]
    driver= '{ODBC Driver 17 for SQL Server}'

    #getting param authid
    authid = req.params.get('authid')

    #if params is empty bad request
    if authid is None:
        return func.HttpResponse(json.dumps({"status":400}))

    #authid isn't empty, so preparing the query.
    query = "select * from [dbo].[HyeAuthentication] where authid = '{}';".format(authid)
    dict = {'table':'HyeAuthentication','status':200,}

    try:
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()


                #bad request 400, there is no record on given authid
                if row == 'null':
                    return func.HttpResponse(json.dumps({"status":400}))

                #success 200
                else:
                    dict['authid'] = row[0]
                    dict['name'] = row[1]
                    dict['phone'] = row[2]
                    dict['email'] = row[3]
                    dict['gender'] = row[4]
                    dict['bike'] = row[5]
                    dict['bicycle'] = row[6]
                    dict['car'] = row[7]

                    return func.HttpResponse(json.dumps(dict))

        
    except:
        return func.HttpResponse(json.dumps({"status":500}))


    

