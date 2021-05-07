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

    #post payload sample
    # {
    # “eventTypeId” : “eventTypeId”,
    # “eventTypeTag” : “eventTypeTag”,
    # “vehicleType” : “vehicleType”,
    # “from_” : “from”,
    # “to_ : “to”,
    # “noSeats” : “noSeats”,
    # “rideDescription” : “rideDescription”,
    # “uid” : “uid”,
    # “rideStartDate” : “rideStartDate”,
    # "actionDate":"actionDate"
    # }


    #preparing the query string with json payload
    query1 = "insert into event values(default,{},'{}','{}','{}','{}',{},'{}',0,'{}','{}','{}');".format(data.get('eventTypeId'),
    data.get('eventTypeTag'),data.get('vehicleType'),data.get('from_'),data.get('to_'),data.get('noSeats'),
    data.get('rideDescription'),data.get('uid'),data.get('rideStartDate'),data.get('pname'))


    query2 = "insert into action values(default,(select eventId from event where uid='{}' and rideStartDate='{}'),'{}',{},'you',1,' posted a ride to {} from {} for {}',1,'{}','{}');".format(
    data.get('uid'),data.get('rideStartDate'),data.get('uid'),data.get('eventTypeId'),data.get('to_'),data.get('from_'),data.get('rideStartDate'),data.get('uid'),data.get('actionDate'))

    try:
        with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query1)
                cursor.execute(query2)
                return func.HttpResponse(json.dumps({"status":200}))
    except:
        return func.HttpResponse(json.dumps({"status":500}))

    
