import logging
import os
import azure.functions as func
import json
import pyodbc



def main(req: func.HttpRequest) -> func.HttpResponse:
    
    data = req.get_json()


    #getting values of application settings 
    server = os.environ['Server']
    database =  os.environ["database"]
    username = os.environ["admin"]
    password = os.environ["password"]
    driver= '{ODBC Driver 17 for SQL Server}'
    

   
    query1 = "Insert into action values(default,CONVERT(UNIQUEIDENTIFIER,'{}'),'{}',1,'{}',0,' has declined your request to {}',7,'{}','{}');".format(
    data.get('eventId'),data.get('requesterUid'),data.get('requesteeName'),data.get('rideDescription'),data.get('requesteeUid'),data.get('actionDate'))

    query2 = "Insert into action values(default,CONVERT(UNIQUEIDENTIFIER,'{}'),'{}',1,'you',0,' declined {} request to  {}',6,'{}','{}');".format(
    data.get('eventId'),data.get('requesteeUid'),data.get('requesterName'),data.get('rideDescription'),data.get('requesteeUid'),data.get('actionDate'))

    query3 = "select  * from action where eventId='{}' and uid='{}' and actionTypeId=7;".format(data.get('eventId'),data.get('requesterUid'))

    if str(data.get("rideStartDate"))>=str(data.get("actionDate")):

        try:
            with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
                with conn.cursor() as cursor:

                    cursor.execute(query3)
                    row = cursor.fetchone()

                    if row is None:
                        cursor.execute(query1)
                        cursor.execute(query2)
                        return func.HttpResponse(json.dumps({"status":200}))
                    else:
                        return func.HttpResponse(json.dumps({"status":400}))

        except:
            return func.HttpResponse(json.dumps({"status":500}))

    else:
        return func.HttpResponse(json.dumps({"status":503}))

