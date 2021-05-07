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
    date = req.params.get('date')

    #if params is empty bad request
    if date is None:
        return func.HttpResponse(json.dumps({"status":400}))

    #authid isn't empty, so preparing the query.
    query = "select * from event where rideStartDate >= '{}';".format(date)
    dict = {'events':[],'status':200,}

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
                        dict['events'].append({'eventId':row[0],'eventTypeId':row[1],'eventTypeTag':row[2]
                        ,'vehicleType':row[3],'from_':row[4],'to_':row[5],'noSeats':row[6],'rideDescription':
                        row[7],'rideCancelled':row[8],'uid':row[9],'rideStartDate':str(row[10]),'pname':str(row[11])})
                        row = cursor.fetchone()

                            
                    return func.HttpResponse(json.dumps(dict))

        
    except:
        return func.HttpResponse(json.dumps({"status":500}))


    

