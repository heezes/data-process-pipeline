
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

    def getBatteryDtcList(self, data):
        dtc_data = []
        if 'data' in data:
            for line in data['data']:
                if (line['data']['fault'] != 16515077) and (line['data']['fault'] != 0) and (line['data']['fault'] != None):
                    dtc_info = {}
                    dtc_info['timestamp'] = line['data']['timestamp']
                    dtc_info['fault'] = line['data']['fault']
                    dtc_data.append(dtc_info)
        else:
            for line in data:
                if (line['fault'] != 16515077) and (line['fault'] != 0) and (line['fault'] != None):
                    dtc_info = {}
                    dtc_info['timestamp'] = line['timestamp']
                    dtc_info['fault'] = line['fault']
                    dtc_data.append(dtc_info)
        return dtc_data

    def getTripStats(self, data):
        total_trips = []
        trip_data = []
        for idx, line in enumerate(data["data"]):
            line["data"]["timestamp"] = line["timestamp"]
            try:
                idx = (len(data["data"])-1) if (idx == (len(data["data"]) -1 )) else idx+1
                if (line["data"]["rideState"] == 3 and data['data'][idx]['data']['rideState'] == 1) or \
                    (line["data"]["rideState"] == 3 and data['data'][idx]['data']['rideState'] == 2):
                    line['data']['tripComplete'] = True
                    trip_data.append(line["data"])
                    total_trips.append(trip_data.copy())
                    trip_data.clear()
                else:
                    trip_data.append(line["data"])
            except Exception as e:
                print(str(e))
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
            dtc = self.getBatteryDtcList(total_trips[i])
            if len(dtc) > 0:
                trip_info['batteryFault'] = dtc
            trip_stats.append(trip_info)
        return trip_stats