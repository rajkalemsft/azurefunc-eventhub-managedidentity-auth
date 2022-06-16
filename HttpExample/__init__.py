from itertools import product
import logging
from HttpExample.testclient import *
import azure.functions as func

from HttpExample.testclient import testclient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    producer = testclient()
    producer.send()

    return func.HttpResponse(
         "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
         status_code=200
    )
