import sys
from textwrap import indent
from Deserializer.aws_uploader import AWSUploader, VIM_REALTIME_DATA,VIM_LOGGED_DATA,VIM_LOGGED_DATA_V2
from Deserializer.deserializer import DeSerializer, BASEDIR
from Deserializer.dataformatter import DataFormatter
from Deserializer.trip_info import tripInfo
import os, json
import time

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
            info = deSerializer.get_info()
            print(f"Discarded Frame: {info['discarded_frames_count']} Found Frame: {info['frame found']}")
            awsuploader=AWSUploader(TABLE_ID=VIM_LOGGED_DATA_V2,DEVICE_ID=self.deviceId,data_dict=formatted_data)
            print(awsuploader.push_to_aws())
            trip = tripInfo()
            # raw_data = trip.arrangeRawData(formatted_data)
            trips = trip.getTripStats(formatted_data)
            if len(trips) > 0:
                awsuploader.push_trips(trips)
            else:
                print("No Trip Found")
            dtc = trip.getBatteryDtcDict(formatted_data)
            if len(dtc) > 0:
                awsuploader.push_dtc(dtc)
            else:
                print("No DTC found in data")
            os.remove(outfilepath)
            print("{}: Upload Successful!".format(time.time()))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(f"{time.time()}: Guru decodeAndUpload Error: {str(e)}")
            pass