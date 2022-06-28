
from multiprocessing.dummy import Array


class tripInfo:
    def __init__(self) -> None:
        pass

    def _getTripTimestamp(self, data):
        if len(data) == 0:
            return None, None
        elif len(data) == 1:
            return [0], None
        else:
            return data[0]['timestamp'], data[-1]['timestamp']

    def _getSocInfo(self, data) -> Array:
        temp_soc = []
        for i in range(0, len(data)):
            temp_soc.append(data[i]['batterySoh'])
        if len(temp_soc) == 0:
            return None, None
        elif len(temp_soc) == 1:
            return temp_soc[0], None
        else:
            val = None
            for i in range(0, (len(temp_soc) if len(temp_soc) < 3 else 3)):
                if  temp_soc[i] != None:
                    val = temp_soc[i]
                    break
            return val, temp_soc[-1]


    def _getSohInfo(self, data) -> Array:
        temp_soh = []
        for i in range(0, len(data)):
            temp_soh.append(data[i]['batterySoh'])
        if len(temp_soh) == 0:
            return None, None
        elif len(temp_soh) == 1:
            return [0], None
        else:
            val = None
            for i in range(0, (len(temp_soh) if len(temp_soh) < 3 else 3)):
                if  temp_soh[i] != None:
                    val = temp_soh[i]
                    break
            return val, temp_soh[-1]


    def _getTripDistance(self, data):
        distance = None
        for i in range(len(data), 0):
            if data[i]["distance"] != None:
                distance = data[i]["distance"]
                break
        return distance

    def _getItemCount(self, data):
        return len(data)

    def getBatteryDtcDict(self, data):
        dtc_data = []
        dtc_dict_keys = [
                    "Over_voltage",
                    "Under_voltage",
                    "Over_temperature",
                    "Under_temperature",
                    "Over_current_discharge",
                    "Over_current_charge",
                    "Short_circuit",
                    "Mosfet_over_temperature", 
                    "Mosfet_under_temperature",
                    "Afe_unresponsive",
                    "Bms_over_temperature",
                    "Bms_under_temperature"]
        if 'data' in data:
            for line in data['data']:
                if (line['data']['fault'] != 16515077) and (line['data']['fault'] != 0) and (line['data']['fault'] != None):
                    dtc_info = {}
                    dtc_info['timestamp'] = line['data']['timestamp']
                    dtc_info['fault'] = line['data']['fault']
                    dtc_data.append(dtc_info)
            return dtc_data
        else:
            dtc_dict = {}
            for key in dtc_dict_keys:
                dtc_dict[key] = 0
            for line in data:
                if (line['fault'] != 16515077) and (line['fault'] != 0) and (line['fault'] != None):
                    bms_code = line['fault']<<8
                    bms = {
                    "Over_voltage":             (bms_code & 0x6000) >> 14,
                    "Under_voltage":            (bms_code & 0xc000) >> 15,
                    "Over_temperature":         (bms_code & 0x010000) >> 16,
                    "Under_temperature":        (bms_code & 0x020000) >> 17,
                    "Over_current_discharge":   (bms_code & 0x040000) >> 18,
                    "Over_current_charge":      (bms_code & 0x080000) >> 19,
                    "Short_circuit":            (bms_code & 0x100000) >> 20,
                    "Mosfet_over_temperature":  (bms_code & 0x200000) >> 21,
                    "Mosfet_under_temperature": (bms_code & 0x400000) >> 22,
                    "Afe_unresponsive":         (bms_code & 0x800000) >> 23,
                    "Bms_over_temperature":     (bms_code & 0x01000000) >> 24,
                    "Bms_under_temperature":    (bms_code & 0x02000000) >> 25
                    }
                    for key in dtc_dict_keys:
                        dtc_dict[key] += bms[key]
            return dtc_dict

    def getTripStats(self, data):
        total_trips = []
        trip_data = []
        about_to_find_ride_end = False
        for idx, line in enumerate(data["data"]):
            line["data"]["timestamp"] = line["timestamp"]
            try:
                idx = (len(data["data"])-1) if (idx == (len(data["data"]) -1 )) else idx+1
                if (line["data"]["rideState"] == 3 and data['data'][idx]['data']['rideState'] == 1) or \
                    (line["data"]["rideState"] == 3 and data['data'][idx]['data']['rideState'] == 2):
                    line['data']['tripComplete'] = True
                    about_to_find_ride_end = False
                    trip_data.append(line["data"])
                    total_trips.append(trip_data.copy())
                    trip_data.clear()
                elif (line["data"]["rideState"] == 1 and data['data'][idx]['data']['rideState'] == 2) or \
                    (line["data"]["rideState"] == 1 and data['data'][idx]['data']['rideState'] == 3):
                    about_to_find_ride_end = False
                    if len(trip_data):
                        temp_line = trip_data[-1]
                        temp_line['data']['tripComplete'] = True
                        trip_data[-1] = temp_line
                        total_trips.append(trip_data.copy())
                        trip_data.clear()
                elif (line["data"]["rideState"] == 2 and data['data'][idx]['data']['rideState'] == 3) or \
                    (about_to_find_ride_end == True):
                    about_to_find_ride_end = True
                    line['data']['tripComplete'] = True
                    trip_data.append(line["data"])
                else:
                    trip_data.append(line["data"])
            except Exception as e:
                print("Error During Trip generation: ", str(e))
                pass
        total_trips.append(trip_data)
        trip_stats = []
        for i in range(len(total_trips)):
            trip_info = {}
            trip_info['startSoc'], trip_info['stopSoc'] = self._getSocInfo(total_trips[i])
            trip_info['startSoh'], trip_info['stopSoh'] = self._getSohInfo(total_trips[i])
            trip_info['startTimestamp'], trip_info['stopTimestamp'] = self._getTripTimestamp(total_trips[i])
            if trip_info['startTimestamp'] != None and trip_info['stopTimestamp'] != None:
                trip_info['tripTime'] = trip_info['stopTimestamp'] - trip_info['startTimestamp']
            else:
                trip_info['tripTime'] = None
            trip_info['distance'] = self._getTripDistance(total_trips[i])
            trip_info['itemCount'] = self._getItemCount(total_trips[i])
            if 'tripComplete' in total_trips[i][-1]:
                trip_info['tripComplete'] = total_trips[i][-1]['tripComplete']
            else:
                trip_info['tripComplete'] = False
            dtc = None
            dtc = self.getBatteryDtcDict(total_trips[i])
            trip_info['batteryFault'] = dtc
            trip_stats.append(trip_info)
        return trip_stats