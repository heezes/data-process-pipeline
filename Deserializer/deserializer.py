
import struct
import json
import os
import datetime
import numpy as np

BASEDIR=os.path.dirname(__file__)

SYNC_CHAR = (0xb5, 0x62)

FRAME_HEADER_FOOTER_LEN = 18

FRAME_LEN_IDX = 2
FRAME_LEN_LEN = 2

FRAME_MSG_IDX = 4
FRAME_MSG_LEN = 6

FRAME_MSKMSG_IDX = 10
FRAME_MSKMSG_LEN = 6

FRAME_DATA_IDX = 16
# offset Note:original length will be calculated from the frame length field
FRAME_DATA_LEN = 0

FRAME_CHKSUM_IDX = FRAME_DATA_LEN + FRAME_HEADER_FOOTER_LEN - 2
FRAME_CHKSUM_LEN = 2


vimloggeddata = {
    "timestamp": 1643537459,
    "data": {
        "vhpd_data": [
            0,
            0,
            0,
            -4,
            -4,
            -4
        ],
        "hpd_data": {
            "rpm": 12204,
            "batteryShuntCurrent": 0,
            "batteryShuntCurrentTimestamp": 0,
            "buckCurrent": -10,
            "throttle": 0
        },
        "npd_data": {
            "batteryThermistorTempTimestamp": 0,
            "batteryThermistorTemp": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "batteryIcTemp": 0,
            "batteryMosfetTemp": 0,
            "distance": 0,
            "brake": 0,
            "coordinates": [
                28.726558685302734,
                77.17229461669922
            ]
        },
        "lpd_data": {
            "batteryCellVoltagesTimestamp": 203266340,
            "batteryCellVoltages": [
                3258,
                3261,
                3258,
                3260,
                3258,
                3261,
                3262,
                3263,
                3263,
                3263,
                3261,
                3264,
                3263,
                3264,
                3255,
                255,
                255,
                255,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "batteryStackVoltage": [
                48923,
                0,
                0,
                0
            ],
            "batterySoc": 40.55117416381836,
            "batterySoh": 100.0,
            "estimatedRange": 0.0,
            "vimIcTemp": -34
        },
        "vlpd_data": None,
        "async_data": {
            "fault": 16515077,
            "batteryId": "VECSTARTBT05"
        }
    }
}


class VIMDecoder:
    def __init__(self, frames) -> None:
        self.__frames = frames
        self.__flags_dict = {
            'epoch_flag': 1,
            'imu_flag': 1,
            'rpm_flag': 1,
            'batteryshuntcurrent_flag': 1,
            'batteryshuntcurrenttimestamp_flag': 1,
            'buckcurrent_flag': 1,
            'throttle_flag': 1,
            'batterythermistortemptimestamp_flag': 1,
            'batteryictemp_flag': 1,
            'batterymosfettemp_flag': 1,
            'distance_flag': 1,
            'brake_flag': 1,
            'coordinates_flag': 1,
            'batterycellvoltagestimestamp_flag': 1,
            'batterycellvoltages_flag': 1,
            'batterysoc_flag': 1,
            'batterysoh_flag': 1,
            'estimatedrange_flag': 1,
            'vimictemp_flag': 1,
            'batteryg4timestamp_flag': 1,
            'batterychgmosstatus_flag': 1,
            'batterydsgmosstatus_flag': 1,
            'batterypremosstatus_flag': 1,
            'batterybalancingstatus_flag': 1,
            'fault_flag': 1,
            'batteryid_flag': 1,
            'reserved0': 6,
            'batterystackvoltage_flag': 4,
            'batterythermistortemp_flag': 4,
            'reserved1': 8
        }

        self.__frame_data_dict = {
            "timestamp": 0,
            "imuAxes": [],
            "rpm": 0,
            "batteryShuntCurrent": 0,
            "batteryShuntCurrentTimestamp": 0,
            "buckCurrent": 0,
            "throttle": 0,
            "batteryThermistorTempTimestamp": 0,
            "batteryThermistorTemp": [],
            "batteryIcTemp": 0,
            "batteryMosfetTemp": 0,
            "distance": 0,
            "brake": 0,
            "coordinates": [],
            "batteryCellVoltagesTimestamp": 0,
            "batteryCellVoltages": [],
            "batteryStackVoltage": [],
            "batterySoc": 0,
            "batterySoh": 0,
            "estimatedRange": 0,
            "vimIcTemp": 0,
            "batteryG4Timestamp": 0,
            "batteryChgMosStatus": 0,
            "batteryDsgMosStatus": 0,
            "batteryPreMosStatus": 0,
            "batteryBalancingStatus": 0,
            "fault": 0,
            "batteryId": []
        }

    def VIMDecoder_decode_frames(self,discarded_frame_decode) -> list:
        decoded_data_list = []
        frames_list = self.__frames.get('frames_list', [])
        if discarded_frame_decode:
            frames_list = self.__frames.get('discarded_frames_list', [])
        for frame in frames_list:
            data_flag = ~frame['frame_mask_flag'] & frame['frame_flag']
            temp = 0
            flags_data_dict = {}
            for key, val in self.__flags_dict.items():
                t = 0
                for i in range(0, val):
                    t |= (1 << i)
                flags_data_dict[key] = (data_flag >> temp) & t
                temp = temp+val

            frame_data_idx = 0

            epoch = None
            rpm = None
            imuAxes = []
            batteryShuntCurrent = None
            batteryShuntCurrentTimestamp = None
            buckCurrent = None
            throttle = None
            batteryThermistorTempTimestamp = None
            batteryThermistorTemp = []
            batteryIcTemp = None
            batteryMosfetTemp = None
            distance = None
            brake = None
            coordinates = []
            batteryCellVoltagesTimestamp = None
            batteryCellVoltages = []
            batteryStackVoltage = []
            batterySoc = None
            batterySoh = None
            estimatedRange = None
            vimIcTemp = None
            batteryG4Timestamp = None
            batteryChgMosStatus = None
            batteryDsgMosStatus = None
            batteryPreMosStatus = None
            batteryBalancingStatus = None
            fault = None
            batteryId = None

            masking_flag = frame['frame_mask_flag']

        # epoch

            if flags_data_dict['epoch_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                epoch = int.from_bytes(temp, byteorder='little', signed=False)
                frame_data_idx += 4

        # imu

            if flags_data_dict['imu_flag']:
                temp1 = []
                temp1 = frame['frame_data'][frame_data_idx:frame_data_idx+12]
                for t in range(0, len(temp1), 2):
                    temp = temp1[t:t+2]
                    imuAxes.append(int.from_bytes(
                        temp, byteorder='little', signed=True))
                frame_data_idx += 12
        # rpm

            if flags_data_dict['rpm_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx + 2]
                rpm = int.from_bytes(temp, byteorder='little', signed=False)
                frame_data_idx += 2

        # batteryShuntCurrent

            if flags_data_dict['batteryshuntcurrent_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                batteryShuntCurrent = int.from_bytes(
                    temp, byteorder='little', signed=True)
                frame_data_idx += 4

        # batteryShuntCurrentTimestamp

            if flags_data_dict['batteryshuntcurrenttimestamp_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                batteryShuntCurrentTimestamp = int.from_bytes(
                    temp, byteorder='little', signed=False)
                frame_data_idx += 4

        # buckCurrent 2b

            if flags_data_dict['buckcurrent_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+2]
                buckCurrent = int.from_bytes(
                    temp, byteorder='little', signed=True)
                frame_data_idx += 2

        # throttle

            if flags_data_dict['throttle_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+2]
                throttle = int.from_bytes(
                    temp, byteorder='little', signed=False)
                frame_data_idx += 2

        # batteryIcTemp

            if flags_data_dict['batteryictemp_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+2]
                batteryIcTemp = int.from_bytes(
                    temp, byteorder='little', signed=True)
                frame_data_idx += 2

        # batteryMosfetTemp

            if flags_data_dict['batterymosfettemp_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+2]
                batteryMosfetTemp = int.from_bytes(
                    temp, byteorder='little', signed=True)
                frame_data_idx += 2

        # distance

            if flags_data_dict['distance_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+2]
                distance = int.from_bytes(
                    temp, byteorder='little', signed=False)
                frame_data_idx += 2

        # brake

            if flags_data_dict['brake_flag']:
                brake = frame['frame_data'][frame_data_idx+0]
                frame_data_idx += 1

        # coordinates

            if flags_data_dict['coordinates_flag']:
                temp1 = frame['frame_data'][frame_data_idx:frame_data_idx+8]
                for i in range(0, len(temp1), 4):
                    temp = bytearray(temp1[i:i+4])
                    coordinates.append(struct.unpack('f', temp)[0])

                frame_data_idx += 8
        # batterySoc

            if flags_data_dict['batterysoc_flag']:
                temp = bytearray(frame['frame_data']
                                 [frame_data_idx:frame_data_idx+4])
                batterySoc = struct.unpack('f', temp)[0]
                frame_data_idx += 4

        # batterySoh

            if flags_data_dict['batterysoh_flag']:
                temp = bytearray(frame['frame_data']
                                 [frame_data_idx:frame_data_idx+4])
                batterySoh = struct.unpack('f', temp)[0]
                frame_data_idx += 4

        # estimatedRange

            if flags_data_dict['estimatedrange_flag']:
                temp = bytearray(frame['frame_data']
                                 [frame_data_idx:frame_data_idx+4])
                estimatedRange = struct.unpack('f', temp)[0]
                frame_data_idx += 4

        # vimIcTemp

            if flags_data_dict['vimictemp_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                vimIcTemp = int.from_bytes(
                    temp, byteorder='little', signed=True)
                frame_data_idx += 4

        # batteryG4Timestamp

            if flags_data_dict['batteryg4timestamp_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                batteryG4Timestamp = int.from_bytes(
                    temp, byteorder='little', signed=False)
                frame_data_idx += 4

        # batteryChgMosStatus

            if flags_data_dict['batterychgmosstatus_flag']:
                batteryChgMosStatus = frame['frame_data'][frame_data_idx+0]
                frame_data_idx += 1

        # batteryDsgMosStatus

            if flags_data_dict['batterydsgmosstatus_flag']:
                batteryDsgMosStatus = frame['frame_data'][frame_data_idx+0]
                frame_data_idx += 1

        # batteryPreMosStatus

            if flags_data_dict['batterypremosstatus_flag']:
                batteryPreMosStatus = frame['frame_data'][frame_data_idx+0]
                frame_data_idx += 1

        # batteryBalancingStatus

            if flags_data_dict['batterybalancingstatus_flag']:
                batteryBalancingStatus = frame['frame_data'][frame_data_idx +
                                                             1] << 8 | frame['frame_data'][frame_data_idx+0]
                frame_data_idx += 2

        # fault

            if flags_data_dict['fault_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                fault = int.from_bytes(temp, byteorder='little', signed=False)
                frame_data_idx += 4

        # need special handling
        # batteryStackVoltage
            if flags_data_dict['batterystackvoltage_flag']:
                temp_flag = flags_data_dict['batterystackvoltage_flag']
                temp1 = []
                for i in range(0, 4):
                    if (temp_flag >> i) & 1 == 1:
                        temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                        batteryStackVoltage.append(int.from_bytes(
                            temp, byteorder='little', signed=False))
                        frame_data_idx += 4

        # batteryCellVoltages
                if flags_data_dict['batterycellvoltages_flag']:
                    for i in range(0, 4):
                        if (temp_flag >> i) & 1 == 1:
                            temp1 = []
                            temp1 = frame['frame_data'][frame_data_idx:frame_data_idx+36]
                            for t in range(0, len(temp1), 2):
                                temp = temp1[t:t+2]
                                batteryCellVoltages.append(int.from_bytes(
                                    temp, byteorder='little', signed=False))
                            frame_data_idx += 36

                # batteryCellVoltagesTimestamp

                if flags_data_dict['batterycellvoltagestimestamp_flag']:
                    temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                    batteryCellVoltagesTimestamp = int.from_bytes(
                        temp, byteorder='little', signed=False)
                    frame_data_idx += 4

            # batteryThermistorTemp

            if flags_data_dict['batterythermistortemp_flag']:
                temp_flag = flags_data_dict['batterythermistortemp_flag']
                temp1 = []
                for i in range(0, 4):
                    if (temp_flag >> i) & 1 == 1:
                        temp1 = []
                        temp1 = frame['frame_data'][frame_data_idx:frame_data_idx+18]
                        for t in range(0, len(temp1), 2):
                            temp = temp1[t:t+2]
                            batteryThermistorTemp.append(int.from_bytes(
                                temp, byteorder='little', signed=True))
                        frame_data_idx += 18

        # batterythermistortemptimestamp_flag

            if flags_data_dict['batterythermistortemptimestamp_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+4]
                batteryThermistorTempTimestamp = int.from_bytes(
                    temp, byteorder='little', signed=False)
                frame_data_idx += 4

        # batteryId

            if flags_data_dict['batteryid_flag']:
                temp = frame['frame_data'][frame_data_idx:frame_data_idx+12]
                batteryId = ''
                for t in temp:
                    batteryId += chr(t)
                frame_data_idx += 12

            frame_data_dict = {
                "flag": flags_data_dict,
                "frame_no": frame['frame_no'],
                "masking_flag": masking_flag,
                "timestamp": epoch,
                "imuAxes": imuAxes,
                "rpm": rpm,
                "batteryShuntCurrent": batteryShuntCurrent,
                "batteryShuntCurrentTimestamp": batteryShuntCurrentTimestamp,
                "buckCurrent": buckCurrent,
                "throttle": throttle,
                "batteryThermistorTempTimestamp": batteryThermistorTempTimestamp,
                "batteryThermistorTemp": batteryThermistorTemp,
                "batteryIcTemp": batteryIcTemp,
                "batteryMosfetTemp": batteryMosfetTemp,
                "distance": distance,
                "brake": brake,
                "coordinates": coordinates,
                "batteryCellVoltagesTimestamp": batteryCellVoltagesTimestamp,
                "batteryCellVoltages": batteryCellVoltages,
                "batteryStackVoltage": batteryStackVoltage,
                "batterySoc": batterySoc,
                "batterySoh": batterySoh,
                "estimatedRange": estimatedRange,
                "vimIcTemp": vimIcTemp,
                "batteryG4Timestamp": batteryG4Timestamp,
                "batteryChgMosStatus": batteryChgMosStatus,
                "batteryDsgMosStatus": batteryDsgMosStatus,
                "batteryPreMosStatus": batteryPreMosStatus,
                "batteryBalancingStatus": batteryBalancingStatus,
                "fault": fault,
                "batteryId": batteryId
            }
            decoded_data_list.append(frame_data_dict.copy())

        return decoded_data_list


class DeSerializer:
    def __init__(self, path: str) -> None:

        self.path = path
        self.__SYNC_CHAR = SYNC_CHAR
        self.__bin_data = self.get_bin_data()
        self.__bin_data_len = len(self.__bin_data)
        self.__frames_indx_list = self.find_frames_idx()
        self.__frame_count = len(self.__frames_indx_list)

        self.frames, self.__recovered_data_len = self.extract_frames()
        if self.__bin_data_len:
            self.loss = (1-(self.__recovered_data_len/self.__bin_data_len))*100
        else:
            self.loss = 100

    def get_info(self) -> dict:
        frame_info = {
            "sync char": SYNC_CHAR,
            "FRAME_HEADER_FOOTER_LEN": FRAME_HEADER_FOOTER_LEN,
            "FRAME_LEN_IDX": FRAME_LEN_IDX,
            "FRAME_LEN_LEN": FRAME_LEN_LEN,
            "FRAME_MSG_IDX": FRAME_MSG_IDX,
            "FRAME_MSG_LEN": FRAME_MSG_LEN,
            "FRAME_MSKMSG_IDX": FRAME_MSKMSG_IDX,
            "FRAME_MSKMSG_LEN": FRAME_MSKMSG_LEN,
            "FRAME_DATA_IDX": FRAME_DATA_IDX,
            "FRAME_DATA_LEN": FRAME_DATA_LEN,
            "FRAME_CHKSUM_IDX": FRAME_CHKSUM_IDX,
            "FRAME_CHKSUM_LEN": FRAME_CHKSUM_LEN
        }
        info = {
            "binary data length": self.__bin_data_len,
            "frame found": self.__frame_count,
            "frame info": frame_info,
            "discarded_frames_count": len(self.frames['discarded_frames_list']),
            "recovered bytes": self.__recovered_data_len,
            "loss(%)": self.loss,

        }

        return info

    def get_bin_data(self) -> list:
        bin_data = []
        try:
            with open(self.path, 'rb') as bin_data_file:
                bin_data = bin_data_file.read()
        except Exception as e:
            print(f"Exception {e} while opening file:{self.path}")
        return bin_data

    def find_frames_idx(self) -> list:
        frames_indx_list = []
        for i in range(0, self.__bin_data_len):
            if self.__bin_data[i] == self.__SYNC_CHAR[0] and self.__bin_data[i+1] == self.__SYNC_CHAR[1]:
                frames_indx_list.append(i)
        return frames_indx_list

    def extract_frames(self) -> dict:
        single_frame_info = {
            "frame_no": 0,
            "frame_len": 0,
            "frame_flag": 0,
            "frame_mask_flag": 0,
            "frame_data": [],
            "frame_checksum": [],
            "frame_calculated_checksum": 0
        }

        data_recovered_count = 0
        frames_list = []
        discarded_frames_list = []
       
        for frame_location_idx in range(0, self.__frame_count):
            tmp_idx = self.__frames_indx_list[frame_location_idx]
            temp_frame_len = 0
            temp_frame_flag = 0
            temp_frame_mask_flag = 0
            temp_frame_data = []
            temp_frame_checksum = []
            try:
                for i in range(0, FRAME_LEN_LEN):
                    temp_frame_len |= self.__bin_data[tmp_idx +
                                                    FRAME_LEN_IDX+i] << (i*8)
                for i in range(0, FRAME_MSG_LEN):
                    temp_frame_flag |= self.__bin_data[tmp_idx +
                                                    FRAME_MSG_IDX+i] << (i*8)
                for i in range(0, FRAME_MSKMSG_LEN):
                    temp_frame_mask_flag |= self.__bin_data[tmp_idx +
                                                            FRAME_MSKMSG_IDX+i] << (i*8)
                for i in range(0, temp_frame_len+FRAME_DATA_LEN):
                    temp_frame_data.append(
                        self.__bin_data[tmp_idx+FRAME_DATA_IDX+i])
                for i in range(0, FRAME_CHKSUM_LEN):
                    temp_frame_checksum.append(
                        self.__bin_data[tmp_idx+temp_frame_len+FRAME_HEADER_FOOTER_LEN-2+i])

                data_recovered_count = data_recovered_count+FRAME_LEN_LEN + \
                    FRAME_MSKMSG_LEN+FRAME_MSG_LEN+temp_frame_len+FRAME_CHKSUM_LEN

                checksum_buf = []
                checksum_buf.extend(
                    self.__bin_data[tmp_idx:tmp_idx+temp_frame_len+FRAME_HEADER_FOOTER_LEN])

                single_frame_info['frame_no'] = frame_location_idx
                single_frame_info['frame_len'] = temp_frame_len
                single_frame_info['frame_flag'] = temp_frame_flag
                single_frame_info['frame_mask_flag'] = temp_frame_mask_flag
                single_frame_info['frame_data'] = temp_frame_data
                single_frame_info['frame_checksum'] = temp_frame_checksum
                single_frame_info['frame_calculated_checksum'] = self.calcultate_checksum(
                    checksum_buf, len=(temp_frame_len+FRAME_HEADER_FOOTER_LEN))

                data_checksum = single_frame_info['frame_checksum']
                calculated_checksum = single_frame_info['frame_calculated_checksum']
                if data_checksum[0] == calculated_checksum[0] and data_checksum[1] == calculated_checksum[1]:
                    frames_list.append(single_frame_info.copy())
                else:
                    discarded_frames_list.append(single_frame_info.copy())
            except Exception as e:
                print(f"Exception while extracting frame no:{frame_location_idx}")
        frames = {
            "frames_list": frames_list,
            "discarded_frames_list": discarded_frames_list
        }

        return frames, data_recovered_count

    def decode_frames(self,discarded_frame_decode=False) -> list:
        vimdecoder = VIMDecoder(self.frames)
        return vimdecoder.VIMDecoder_decode_frames(discarded_frame_decode=discarded_frame_decode)

    def calcultate_checksum(self, data, len):
        ck_a = 0
        ck_b = 0
        for i in range(2, len-2):
            ck_a += data[i]
            ck_b += ck_a
        ck_a &= 0xFF
        ck_b &= 0xFF
        return ck_a, ck_b


