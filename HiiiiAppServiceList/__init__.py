import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    return func.HttpResponse(json.dumps({"status":200,
    "ServiceList":[{"title":"Share ride","description":"Share your car and bike rides.","color":"#8FFF29"},
    {"title":"Sell","description":"Sell your products on Hiiii App","color":"#ffffff"},
    {"title":"Events","description":"...","color":"#00ffff"},
    {"title":"Meets","description":"...","color":"#4000ff"}]}))
    
