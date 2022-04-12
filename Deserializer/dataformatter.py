import json,time,os

class DataFormatter:
    def __init__(self, path) -> None:
        self.__path = path
        self.__data_to_format=self.get_json_data()
        self.formatted_vimloggeddata=self.vimloggeddata_formatter()
    def get_json_data(self)->dict:
        jsondata={}
        try:
            with open(self.__path,'r') as f:
                jsondata=json.loads(f.read())
        except Exception as e:
            print(f"Exception {e} occured while opening file {self.__path}")
        return jsondata
    def vimloggeddata_formatter(self)->dict:
        datalist=self.__data_to_format.get("data_list",[])
        formatted_data_list=[]
        for data in datalist:
            epoch=data.get("timestamp",0)
            if epoch:
                temp_dict= {
                    "timestamp": epoch,
                    "data": {
                        "vhpd_data": data.get("imuAxes",[]),
                        "hpd_data": {
                            "rpm": data.get("rpm",0),
                            "batteryShuntCurrent": data.get("batteryShuntCurrent",0) if data.get("batteryShuntCurrent",0) is not None else 0,
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
                            "batterySoc": data.get("batterySoc",0) if data.get("batterySoc",0) is not None else 0,
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
                formatted_data_list.append(temp_dict.copy())

        out_dict={
            "count":len(formatted_data_list),
            "data":formatted_data_list
        }

        return out_dict


