import logging
import os
import azure.functions as func
import json
import pyodbc
import smtplib, ssl
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    data = req.get_json()

    noSeats = 0

    #getting values of application settings 
    server = os.environ['Server']
    database =  os.environ["database"]
    username = os.environ["admin"]
    password = os.environ["password"]
    driver= '{ODBC Driver 17 for SQL Server}'
  
    # writeEmail(data)
    # return func.HttpResponse('email')
    # data = {
    #     "requesterUid":"OLbp05jFuUcNZp2A6LWCQb1hOC62",
    #     "requesteeUid":"temjXq5Zvrcexcu4wxoxKjA6kBR2",
    #     "eventId":"dcbe3462-5d95-47e7-8652-0ef6904b6069",
    #     "requesterName":"Balaji R",
    #     "requesteeName":"A P Rajkumar",
    #     "rideDescription": "Bagalur, Bengalure, Karnataka -> WonderLa, Bengaluru, Karnataka",
    #     "actionDate":"2021-04-28 05:30",
    #     "rideStartDate":"2021-04-29 05:30",
    # }

    query0 = "select noSeats from event where eventId='{}';".format( data.get('eventId'))

    

    url = "https://prod-20.centralindia.logic.azure.com:443/workflows/ef90931246c1448a8c19c0e6226f014a/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=vRp8LYs67gM_1iOQwMpZty_GUlMCBEKP0s7-GxQu-jE"


    headers = {
        'Content-Type': 'application/json'
        }                      
    

    query3 = "select  * from action where eventId='{}' and uid='{}' and actionTypeId=4;".format(data.get('eventId'),data.get('requesterUid'))

    query4 = "select * from HyeAuthentication where authid='{}'".format(data.get('requesterUid'))

    query5 = "select * from HyeAuthentication where authid='{}'".format(data.get('requesteeUid'))


    if str(data.get("rideStartDate"))>=str(data.get("actionDate")):

        try:
            with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
                with conn.cursor() as cursor:

                    cursor.execute(query0)
                    row = cursor.fetchone()

                    if int(row[0])>=1:
                        noSeats = int(row[0])
                        cursor.execute(query3)
                        row = cursor.fetchone()

                        if row is None:
                            currentSeats = lambda s: s-1 if s>=2 else 0
                            query6 = "update event set noSeats = {} where eventId='{}';".format(currentSeats(noSeats),data.get('eventId'))
                            cursor.execute(query6)
                            cursor.execute(query5)
                            row = cursor.fetchone()
                            data['requesteeEmail'] = row[3]
                            data['requesteeName'] = row[1]
                            data['requesteePhone'] = row[2]
                            data['ride'] = data.get('rideDescription')[19:]

                            cursor.execute(query4)
                            row = cursor.fetchone()
                            data['requesterEmail'] = row[3]
                            data['requesterPhone'] = row[2]
                         


                            query2 = "Insert into action values(default,CONVERT(UNIQUEIDENTIFIER,'{}'),'{}',1,'{}',0,' accepted your request {}',4,'{}','{}');".format(
                            data.get('eventId'),data.get('requesterUid'),data.get('requesteeName'),data.get('rideDescription')
                            ,data.get('requesteeUid'),data.get('actionDate'))

                            query1 = "Insert into action values(default,CONVERT(UNIQUEIDENTIFIER,'{}'),'{}',1,' ',0,'you accepted {} request  to {}',5,'{}','{}');".format(
                            data.get('eventId'),data.get('requesteeUid'),data.get('requesterName'),data.get('rideDescription'),
                            data.get('requesteeUid'),data.get('actionDate'))

                            cursor.execute(query1)
                            cursor.execute(query2)
                           
                            requests.request("POST", url, headers=headers, data=json.dumps(data))
                           
                            
                            return func.HttpResponse(json.dumps({"status":200}))
                      

                        else:
                            return func.HttpResponse(json.dumps({"status":400}))

                    else:
                        return func.HttpResponse(json.dumps({"status":504}))



        except:
            return func.HttpResponse(json.dumps({"status":500}))


    else:
        return func.HttpResponse(json.dumps({"status":503}))




# def writeEmail(data):

#     # emailId = "dev.hiiiiapp@gmail.com"
#     # # os.environ['Email_ActionTypeId5']
#     # emailPwd = "fuckworldbyB$1"
#     # # os.environ['EmailPwd_ActionTypeId5']
#     # smtp_server = "smtp.sendgrid.net"
#     # port = 587  
 

#     # context = ssl.create_default_context()

#     # message = MIMEMultipart("alternative")
#     # message["Subject"] = "{} accepted your Ride Request | {}".format(data.get('requesteeName'),data.get('rideDescription')[19:])
#     # message["From"] = 'dev.hiiiiapp@gmail.com'
#     # message["To"] = data.get('requesterInfo')[3]
#     # message["CC"] = data.get('requesteeInfo')[3]

    

#     # Create the plain-text and HTML version of your message
#     text = """\
#     Hi there,

#     your ride request has been accepted

#     Ride details
#     Ride:{}
#     Ride Start : {}

#     Ride Provider details
#         name : {}
#         email : dev.hiiiiapp@gmail.com
#         phone : 
#         rating : 5.0

#     Have a safe journey
    
#     -Hiiii App""".format(data.get('rideDescription'),data.get('rideStartDate'),data.get('requesteeName'))


#     html = """\
#     <html>
#     <head>
#     <style>
#     .content {
#     max-width: 500px;
#     margin: auto;
#     background-color:black;
#     align-content:center;
#     border-radius:35px;
#     font-size:16px;
#     color:white;
#     padding:30px;
#     }
#     </style>
#     </head>
#     <body class="content">
#         <p>Hi """+data['requesterName']+""",<br>
#         <br>
#         """+data['requesteeName']+""" accepted your ride request...<br>
#         <br>
#         <br>
#         Ride details<br>
#         Ride : """+data.get('rideDescription')[19:]+"""<br>
#         Ride Start :"""+data.get('rideStartDate')+""" <br>
#         <br>
#         <br>
#         Ride provider details<br>
#         <br>
#         Name  : """+data.get('requesteeName')+"""<br>
#         phone : """+data.get('requesteeInfo')[2]+"""<br>
#         email : """+data.get('requesteeInfo')[3]+"""<br>
#         Hiiii App Rating : 5.0<br>
#         <br>
#         Have a safe journey
#         <br>
#         -Hiiii App<br>
#         <a href="https://hye-secondary.z29.web.core.windows.net/">Hiiii App</a> 
#         </p>
#     </body>
#     </html>
#     """


    
#     #     <br>
#     # Turn these into plain/html MIMEText objects
#     # part1 = MIMEText(text, "plain")
#     # part2 = MIMEText(html, "html")
#     # message.attach(part1)
#     # message.attach(part2)


#     # message = Mail(
#     # from_email='dev.hiiiiapp@gmail.com',
#     # to_emails= data.get('requesterInfo')[3],
#     # subject="{} accepted your Ride Request | {}".format(data.get('requesteeName'),data.get('rideDescription')[19:]),
#     # html_content=html)
#     # try:
#     #     sg = SendGridAPIClient(os.environ.get('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'))
#     #     logging.info('email sent sucessfully')
#     # except Exception as e:
#     #     logging.info(e.message)
#     # try:
#     #     server = smtplib.SMTP(smtp_server,port)
#     #     server.starttls(context=context)
#     #     server.login(emailId, emailPwd)
#     #     server.sendmail(from_addr='dev.hiiiiapp@gmail.com',to_addrs=[data.get('requesteeInfo')[3],data.get('requesterInfo')[3]], msg=message.as_string())

#     # except Exception as e:
#     #     logging.info(e)
#     message = {
#         "personalizations": [ {
#           "to": [{
#             "email": data.get('requesterInfo')[3]
#             }]}],
#         "subject": "hell world",
#         "content": [{
#             "type": "text/plain",
#             "value": "hello world" }]}

#     sendGridMessage.set(json.dumps(message))
#     logging.info('email sent sucessfully')
    

    
   
        