from pynamodb.models import Model
from pynamodb.attributes import NullAttribute, NumberAttribute, UnicodeAttribute, JSONAttribute, UnicodeSetAttribute,ListAttribute,BooleanAttribute, UTCDateTimeAttribute
import json
import os,time

VIM_REALTIME_DATA=1
VIM_LOGGED_DATA=2


class Vim_Logged_Data(Model):
    class Meta:
        os.environ["TABLE_NAME"] = "vim_logged_data"
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    device_id       =   UnicodeAttribute(hash_key=True)
    timestamp       =   NumberAttribute(range_key=True)
    vhpd_data       =   JSONAttribute(null=True)
    hpd_data        =   JSONAttribute(null=True)
    npd_data        =   JSONAttribute(null=True)
    lpd_data        =   JSONAttribute(null=True)
    vlpd_data       =   JSONAttribute(null=True)
    async_data      =   JSONAttribute(null=True)

class VimUser(Model):
    class Meta:
        os.environ["TABLE_NAME"] = "vim_user_data"        
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    API_ID       =   UnicodeAttribute(hash_key=True)
    USER_NAME = UnicodeAttribute()
    USER_STATUS   =   BooleanAttribute(default=False)
    DEVICE_LIST   =   ListAttribute()
    USER_ID       =   UnicodeAttribute()
    PREFIX  = UnicodeAttribute()
    HASHED_KEY=UnicodeAttribute()
    CREATED_AT = UTCDateTimeAttribute()
    EXPIRY_ON = UTCDateTimeAttribute()
    REVOKED = BooleanAttribute(default=False)

class Vim_Realtime_Data(Model):
    class Meta:
        os.environ["TABLE_NAME"] = "vim_realtime_data"
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = 'us-east-1'
    device_id       =   UnicodeAttribute(hash_key=True)
    timestamp       =   NumberAttribute(range_key=True)
    cell_info       =   UnicodeAttribute(null=True)
    gps             =   ListAttribute(null=True)
    km              =   ListAttribute(null=True)
    soc             =   NumberAttribute(null=True)
    vsr             =   NumberAttribute(null=True)




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
    def __init__(self,TABLE_ID:int,DEVICE_ID:str,data_dict:dict) -> None:
        self.__table_type=TABLE_ID
        self.__device_id=DEVICE_ID
        self.__datalist=data_dict.get('data',[])
    def push_to_aws(self):
        logs=[]
        print(f"Upoading data to tableid:{self.__table_type} deviceid:{self.__device_id}")
        if self.__table_type==VIM_LOGGED_DATA:
            # uploadingbar=tqdm(total=len(self.__datalist))
            # uploaded_counts=0
            for data in self.__datalist:
                with Vim_Logged_Data.batch_write(auto_commit=True) as  batch:
                    try:
                        ts=data.get('timestamp')
                        if ts:
                            data_temp=data.get('data',{})
                            item = Vim_Logged_Data(self.__device_id,ts,
                            vhpd_data   =   data_temp.get('vhpd_data',None),
                            hpd_data    =   data_temp.get('hpd_data',None),
                            npd_data    =   data_temp.get('npd_data',None),
                            lpd_data    =   data_temp.get('lpd_data',None),
                            vlpd_data   =   data_temp.get('vlpd_data',None),
                            async_data  =   data_temp.get('async_data',None))
                            batch.save(item)
                            # uploadingbar.update(1)
                            # uploaded_counts+=1
                            time.sleep(0.065)
                    except Exception as e:
                        logs.append(f'Exception {e} occured during to data upload')
                        print(e)
                        pass
            # print("counts uploaded:", uploaded_counts)
        elif self.__table_type==VIM_REALTIME_DATA:
            pass

        return logs