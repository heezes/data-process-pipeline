from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import os
import time
import boto3


class deviceShawdow:
    def __init__(self, group):
        self.things = None
        self.awsIot = None
        self.deviceShadow = {}
        try:
            client = boto3.client(service_name='iot',                                               \
                                aws_access_key_id="AKIAQMM3NAM3S5B6ED73",                           \
                                aws_secret_access_key="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",   \
                                region_name="us-east-1")
            response = client.list_things_in_thing_group(maxResults=123, thingGroupName=group)
            self.things = response['things']

            self.awsIot = AWSIoTMQTTShadowClient("data-process-pipeline-client", useWebsocket=True)
            self.awsIot.configureEndpoint("a3fu7wrc8e12x7-ats.iot.us-east-1.amazonaws.com", 443)
            self.awsIot.configureIAMCredentials(AWSAccessKeyID = "AKIAQMM3NAM3S5B6ED73", AWSSecretAccessKey = "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")
            self.awsIot.configureCredentials(f"{os.path.dirname(__file__)}/root.crt")
            self.awsIot.configureConnectDisconnectTimeout(10)  # 10 sec
            self.awsIot.configureMQTTOperationTimeout(5)  # 5 sec
            self.awsIot.connect()
            for item in self.things:
                self.deviceShadow[str(item)] = self.awsIot.createShadowHandlerWithName(str(item), True)
        except:
            pass

    def getThingList(self):
        return self.things

    def getDeviceShadow(self, deviceId, callback):
        try:
            self.deviceShadow[str(deviceId)].shadowGet(callback, 10)
        except:
            self.awsIot.disconnect()
            time.sleep(5)
            self.awsIot.connect()
            pass
