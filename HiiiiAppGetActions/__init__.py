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
    uid = req.params.get('uid')

    #if params is empty bad request
    if uid is None:
        return func.HttpResponse(json.dumps({"status":400}))

    #authid isn't empty, so preparing the query.
    query = "select * from action where uid = '{}' order by actionDate DESC;".format(uid)
    dict = {'actions':[],'status':200,}

    try:
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()


                #bad request 204, there is no record on given authid
                if row is None:
                    return func.HttpResponse(json.dumps({"status":204}))

                # #success 200
                else:
                    while row:
                        dict['actions'].append({'aid':row[0],'eventId':row[1],'uid':row[2]
                        ,'eventTypeId':row[3],'name':row[4],'Accepted':row[5],'actionDescription':
                        row[6],'actionTypeId':row[7],'actioneeAid':row[8]})
                        row = cursor.fetchone()

                    return func.HttpResponse(json.dumps(dict))

        
    except:
        return func.HttpResponse(json.dumps({"status":500}))


    

