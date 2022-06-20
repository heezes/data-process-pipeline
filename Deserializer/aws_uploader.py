from pynamodb.models import Model
from pynamodb.attributes import NullAttribute, NumberAttribute, UnicodeAttribute, JSONAttribute, UnicodeSetAttribute, ListAttribute, BooleanAttribute, UTCDateTimeAttribute
import json
import os
import time
# from tqdm import tqdm

VIM_REALTIME_DATA = 1
VIM_LOGGED_DATA = 2
VIM_LOGGED_DATA_V2 = 3

# f = open(f'{os.path.dirname(__file__)}/cred.json', 'r')
# cred = json.loads(f.read())
# f.close()


class Vim_Logged_Data(Model):
    class Meta:
        # os.environ["TABLE_NAME"] = "vim_logged_data"
        # os.environ["AWS_ACCESS_KEY_ID"] = cred['AWS_ACCESS_KEY_ID']
        # os.environ["AWS_SECRET_ACCESS_KEY"] = cred['AWS_SECRET_ACCESS_KEY']
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    device_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    vhpd_data = JSONAttribute(null=True)
    hpd_data = JSONAttribute(null=True)
    npd_data = JSONAttribute(null=True)
    lpd_data = JSONAttribute(null=True)
    vlpd_data = JSONAttribute(null=True)
    async_data = JSONAttribute(null=True)


class Vim_Logged_Trips_V2(Model):
    class Meta:
        table_name = os.environ["TRIP_TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        region = 'us-east-1'
    device_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    itemCounts = NumberAttribute(null=True)
    startSoc = NumberAttribute(null=True)
    stopSoc = NumberAttribute(null=True)
    startSoh = NumberAttribute(null=True)
    stopSoh = NumberAttribute(null=True)
    startTimestamp = NumberAttribute(null=True)
    stopTimestamp = NumberAttribute(null=True)
    tripDistance = NumberAttribute(null=True)
    tripTime = NumberAttribute(null=True)
    batteryFault = ListAttribute(null=True)

class Vim_Logged_Dtc_V2(Model):
    class Meta:
        table_name = os.environ["DTC_TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        region = 'us-east-1'
    device_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    code = NumberAttribute(null=True)
    source = UnicodeAttribute(null=True)

class Vim_Logged_Data_V2(Model):
    class Meta:
        # os.environ["TABLE_NAME"] = "vim_logged_data_v2"
        # os.environ["AWS_ACCESS_KEY_ID"] = cred['AWS_ACCESS_KEY_ID']
        # os.environ["AWS_SECRET_ACCESS_KEY"] = cred['AWS_SECRET_ACCESS_KEY']
        table_name = os.environ["TABLE_NAME_V2"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    device_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    rideStart=BooleanAttribute(null=True)
    rpm = NumberAttribute(null=True)
    imuAxes = ListAttribute(null=True)
    batteryShuntCurrent = NumberAttribute(null=True)
    batteryShuntCurrentTimestamp = NumberAttribute(null=True)
    buckCurrent = NumberAttribute(null=True)
    throttle = NumberAttribute(null=True)
    batteryThermistorTempTimestamp = NumberAttribute(null=True)
    batteryThermistorTemp = ListAttribute(null=True)
    batteryIcTemp = NumberAttribute(null=True)
    batteryMosfetTemp = NumberAttribute(null=True)
    distance = NumberAttribute(null=True)
    brake = NumberAttribute(null=True)
    coordinates = ListAttribute(null=True)
    batteryCellVoltagesTimestamp = NumberAttribute(null=True)
    batteryCellVoltages = ListAttribute(null=True)
    batteryStackVoltage = ListAttribute(null=True)
    batterySoc = NumberAttribute(null=True)
    batterySoh = NumberAttribute(null=True)
    estimatedRange = NumberAttribute(null=True)
    vimIcTemp = NumberAttribute(null=True)
    batteryG4Timestamp = NumberAttribute(null=True)
    batteryChgMosStatus = NumberAttribute(null=True)
    batteryDsgMosStatus = NumberAttribute(null=True)
    batteryPreMosStatus = NumberAttribute(null=True)
    batteryBalancingStatus = NumberAttribute(null=True)
    fault = NumberAttribute(null=True)
    batteryId = UnicodeAttribute(null=True)


class VimUser(Model):
    class Meta:
        # os.environ["TABLE_NAME"] = "vim_user_data"
        # os.environ["AWS_ACCESS_KEY_ID"] = cred['AWS_ACCESS_KEY_ID']
        # os.environ["AWS_SECRET_ACCESS_KEY"] = cred['AWS_SECRET_ACCESS_KEY']
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    API_ID = UnicodeAttribute(hash_key=True)
    USER_NAME = UnicodeAttribute()
    USER_STATUS = BooleanAttribute(default=False)
    DEVICE_LIST = ListAttribute()
    USER_ID = UnicodeAttribute()
    PREFIX = UnicodeAttribute()
    HASHED_KEY = UnicodeAttribute()
    CREATED_AT = UTCDateTimeAttribute()
    EXPIRY_ON = UTCDateTimeAttribute()
    REVOKED = BooleanAttribute(default=False)


class Vim_Realtime_Data(Model):
    class Meta:
        # os.environ["TABLE_NAME"] = "vim_realtime_data"
        # os.environ["AWS_ACCESS_KEY_ID"] = cred['AWS_ACCESS_KEY_ID']
        # os.environ["AWS_SECRET_ACCESS_KEY"] = cred['AWS_SECRET_ACCESS_KEY']
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    device_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    cell_info = UnicodeAttribute(null=True)
    gps = ListAttribute(null=True)
    km = ListAttribute(null=True)
    soc = NumberAttribute(null=True)
    vsr = NumberAttribute(null=True)


class AWSUploader:
    """
for vim looged table
temp_dict= {
            "timestamp": epoch,
            "data": {
                "vhpd_data": data.get("imuAxes",[]),
                "hpd_data": {
                    "rpm": data.get("rpm",0),
                    "batteryShuntCurrent": data.get("batteryShuntCurrent",0),
                    "batteryShuntCurrentTimestamp": data.get("batteryShuntCurrentTimestamp",0),
                    "buckCurrent": data.get("buckCurrent",0),
                    "throttle": data.get("throttle",0)
                },
                "npd_data": {
                    "batteryThermistorTempTimestamp": data.get("batteryThermistorTempTimestamp",0),
                    "batteryThermistorTemp": data.get("batteryThermistorTemp",[]),
                    "batteryIcTemp": data.get("batteryIcTemp",0),
                    "batteryMosfetTemp": data.get("batteryMosfetTemp",0),
                    "distance": data.get("distance",0),
                    "brake": data.get("brake",0),
                    "coordinates": data.get("coordinates",[])
                },
                "lpd_data": {
                    "batteryCellVoltagesTimestamp": data.get("batteryCellVoltagesTimestamp",0),
                    "batteryCellVoltages": data.get("batteryCellVoltages",[]),
                    "batteryStackVoltage": data.get("batteryStackVoltage",[]),
                    "batterySoc": data.get("batterySoc",0),
                    "batterySoh": data.get("batterySoh",0),
                    "estimatedRange": data.get("estimatedRange",0),
                    "vimIcTemp": data.get("vimIcTemp",0)
                },
                "vlpd_data": None,
                "async_data": {
                    "fault": data.get("fault",0),
                    "batteryId": data.get("batteryId","")
                }
            }
        }

data_dict={
    "count": 0,
    "data":list of temp_dicts
}
"""

    def __init__(self, TABLE_ID: int, DEVICE_ID: str, data_dict: dict) -> None:
        self.__table_type = TABLE_ID
        self.__device_id = DEVICE_ID
        self.__datalist = data_dict.get('data', [])

    def push_trips(self, trips):
        for trip in trips:
            with Vim_Logged_Trips_V2.batch_write(auto_commit=True) as batch:
                try:
                    ts = trip['startTimestamp']
                    if ts != None:
                        item = Vim_Logged_Trips_V2(self.__device_id, ts,
                                itemCounts = trip['itemCount'],
                                startSoc = trip['startSoc'],
                                stopSoc = trip['stopSoc'],
                                startSoh = trip['startSoh'],
                                stopSoh = trip['stopSoh'],
                                startTimestamp = trip['startTimestamp'],
                                stopTimestamp = trip['stopTimestamp'],
                                tripDistance = trip['distance'],
                                tripTime = trip['tripTime'],
                                batteryFault = trip['batteryFault'] if 'batteryFault' in trip else None)
                        batch.save(item)
                        time.sleep(0.065)
                except Exception as e:
                    print(e)
                    pass

    def push_dtc(self, dtc):
        for code in dtc:
            with Vim_Logged_Dtc_V2.batch_write(auto_commit=True) as batch:
                try:
                    ts = code['timestamp']
                    if ts != None:
                        item = Vim_Logged_Dtc_V2(self.__device_id, ts,
                                code = code['fault'],
                                source = "Battery")
                        batch.save(item)
                        time.sleep(0.065)
                except Exception as e:
                    print(str(e))
                    pass

    def push_to_aws(self):
        logs = []
        print(
            f"Upoading data to tableid:{self.__table_type} deviceid:{self.__device_id}")
        if self.__table_type == VIM_LOGGED_DATA:
            # uploadingbar = tqdm(total=len(self.__datalist))
            # uploaded_counts = 0
            for data in self.__datalist:
                with Vim_Logged_Data.batch_write(auto_commit=True) as batch:
                    try:
                        ts = data.get('timestamp')
                        if ts:
                            data_temp = data.get('data', {})
                            item = Vim_Logged_Data(self.__device_id, ts,
                                                   vhpd_data=data_temp.get(
                                                       'vhpd_data', None),
                                                   hpd_data=data_temp.get(
                                                       'hpd_data', None),
                                                   npd_data=data_temp.get(
                                                       'npd_data', None),
                                                   lpd_data=data_temp.get(
                                                       'lpd_data', None),
                                                   vlpd_data=data_temp.get(
                                                       'vlpd_data', None),
                                                   async_data=data_temp.get('async_data', None))
                            batch.save(item)
                            # uploadingbar.update(1)
                            # uploaded_counts += 1
                            time.sleep(0.065)
                    except Exception as e:
                        logs.append(
                            f'Exception {e} occured during to data upload')
                        print(e)
                        pass
            # print("counts uploaded:", uploaded_counts)
        elif self.__table_type == VIM_REALTIME_DATA:
            pass
        elif self.__table_type == VIM_LOGGED_DATA_V2:
            # uploadingbar = tqdm(total=len(self.__datalist))
            uploaded_counts = 0
            for data in self.__datalist:
                with Vim_Logged_Data_V2.batch_write(auto_commit=True) as batch:
                    try:
                        ts = data.get('timestamp')
                        if ts:
                            data_temp = data.get('data', {})
                            item = Vim_Logged_Data_V2(self.__device_id, ts,
                                                        rideStart=data_temp.get(
                                                          'RideStart', None),
                                                      rpm=data_temp.get(
                                                          'rpm', None),
                                                      imuAxes=data_temp.get(
                                                          'imuAxes', None),
                                                      batteryShuntCurrent=data_temp.get(
                                                          'batteryShuntCurrent', None),
                                                      batteryShuntCurrentTimestamp=data_temp.get(
                                                          'batteryShuntCurrentTimestamp', None),
                                                      buckCurrent=data_temp.get(
                                                          'buckCurrent', None),
                                                      throttle=data_temp.get(
                                                          'throttle', None),
                                                      batteryThermistorTempTimestamp=data_temp.get(
                                                          'batteryThermistorTempTimestamp', None),
                                                      batteryThermistorTemp=data_temp.get(
                                                          'batteryThermistorTemp', None),
                                                      batteryIcTemp=data_temp.get(
                                                          'batteryIcTemp', None),
                                                      batteryMosfetTemp=data_temp.get(
                                                          'batteryMosfetTemp', None),
                                                      distance=data_temp.get(
                                                          'distance', None),
                                                      brake=data_temp.get(
                                                          'brake', None),
                                                      coordinates=data_temp.get(
                                                          'coordinates', None),
                                                      batteryCellVoltagesTimestamp=data_temp.get(
                                                          'batteryCellVoltagesTimestamp', None),
                                                      batteryCellVoltages=data_temp.get(
                                                          'batteryCellVoltages', None),
                                                      batteryStackVoltage=data_temp.get(
                                                          'batteryStackVoltage', None),
                                                      batterySoc=data_temp.get(
                                                          'batterySoc', None),
                                                      batterySoh=data_temp.get(
                                                          'batterySoh', None),
                                                      estimatedRange=data_temp.get(
                                                          'estimatedRange', None),
                                                      vimIcTemp=data_temp.get(
                                                          'vimIcTemp', None),
                                                      batteryG4Timestamp=data_temp.get(
                                                          'batteryG4Timestamp', None),
                                                      batteryChgMosStatus=data_temp.get(
                                                          'batteryChgMosStatus', None),
                                                      batteryDsgMosStatus=data_temp.get(
                                                          'batteryDsgMosStatus', None),
                                                      batteryPreMosStatus=data_temp.get(
                                                          'batteryPreMosStatus', None),
                                                      batteryBalancingStatus=data_temp.get(
                                                          'batteryBalancingStatus', None),
                                                      fault=data_temp.get(
                                                          'fault', None),
                                                      batteryId=data_temp.get(
                                                          'batteryId', None))
                            batch.save(item)
                            # uploadingbar.update(1)
                            uploaded_counts += 1
                            time.sleep(0.065)
                    except Exception as e:
                        logs.append(
                            f'Exception {e} occured during to data upload')
                        # print(e)
                        pass
            print(f"Uploaded: {uploaded_counts} out of {len(self.__datalist)}")

        return logs
