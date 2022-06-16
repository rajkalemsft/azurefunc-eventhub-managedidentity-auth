import time
from confluent_kafka import Producer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
import logging

class testclient:
    FULLY_QUALIFIED_NAMESPACE =""
    EVENTHUB_NAME = ""
    AUTH_SCOPE = ""

    def __init__(self):
        load_dotenv()
        self.FULLY_QUALIFIED_NAMESPACE= os.environ['EVENT_HUB_HOSTNAME']
        self.EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']
        self.AUTH_SCOPE= "https://" + self.FULLY_QUALIFIED_NAMESPACE +"/.default"
        

    def _get_token(self, config):
        # AAD
        FULLY_QUALIFIED_NAMESPACE= os.environ['EVENT_HUB_HOSTNAME']
        EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']
        AUTH_SCOPE= "https://" + FULLY_QUALIFIED_NAMESPACE +"/.default"
        cred = DefaultAzureCredential()
        access_token = cred.get_token(AUTH_SCOPE)
        return access_token.token, time.time() + access_token.expires_on 
    
    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logging.info(f"Message delivery failed: {err}")
        else:
            logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send(self):
        producer = Producer({
        "bootstrap.servers": self.FULLY_QUALIFIED_NAMESPACE + ":9093",
        "sasl.mechanism": "OAUTHBEARER",
        "security.protocol": "SASL_SSL",
        "oauth_cb": self._get_token,
        "enable.idempotence": True,
        "acks": "all",
        # "debug": "broker,topic,msg"
        })

        some_data_source = [str(i) for i in range(1000)]
        for data in some_data_source:
            # Trigger any available delivery report callbacks from previous produce() calls
            producer.poll(0)

            # Asynchronously produce a message, the delivery report callback
            # will be triggered from poll() above, or flush() below, when the message has
            # been successfully delivered or failed permanently.
            producer.produce(self.EVENTHUB_NAME, data.encode("utf-8"), callback=self.delivery_report)

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        producer.flush()