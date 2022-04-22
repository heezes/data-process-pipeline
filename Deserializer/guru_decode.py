from textwrap import indent
from Deserializer.aws_uploader import AWSUploader, VIM_REALTIME_DATA,VIM_LOGGED_DATA,VIM_LOGGED_DATA_V2
from Deserializer.deserializer import DeSerializer, BASEDIR
from Deserializer.dataformatter import DataFormatter
import os, json

class ProcessRawData():
    def __init__(self, filepath):
        filename = filepath.split("data/")[1]
        temp = filename.split(".")[0].split("-")
        self.deviceId = temp[0]+"-"+temp[1]+"-"+temp[2]
        pass

    def decodeAndUpload(self, filepath):
        try:
            deSerializer = DeSerializer(filepath)
            deSerialized_data = {"data_list": deSerializer.decode_frames()}
            outfilepath=f"{BASEDIR}/data.json"
            f = open(outfilepath, "w")
            f.write(json.dumps(deSerialized_data, indent=4))
            f.close()
            vimformatter=DataFormatter(outfilepath)
            formatted_data=vimformatter.vimloggeddata_v2_formatter()
            awsuploader=AWSUploader(TABLE_ID=VIM_LOGGED_DATA_V2,DEVICE_ID=self.deviceId,data_dict=formatted_data)
            print(awsuploader.push_to_aws())
            os.remove(outfilepath)
        except:
            print("Guru decodeAndUpload Error!")
            pass