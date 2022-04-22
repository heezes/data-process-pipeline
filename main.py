try:
    import jfwEncoderDecoder.jfw_deserializer as jfw
except:
    pass
from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute, JSONAttribute
from pathlib import Path
import json
import os
import glob
import shutil
import logging
from logging.handlers import RotatingFileHandler
from functools import partial
import pygeohash as gh
# import firebase_db
import iot
import time
from Deserializer import guru_decode
 

def customCallback(payload, responseStatus, token, id=None):
    global db
    jdata = json.loads(payload)
    soc = None
    gps = None
    tempdata = {}
    try:
        soc = jdata["state"]["reported"]["soc"]
        gps = jdata["state"]["reported"]["gps"]
    except:
        pass
    if soc != None:
        tempdata['soc'] = soc
    if gps != None:
        tempdata['l'] = {'0':float(gps[0]), '1':float(gps[1])}
        tempdata['g'] = gh.encode(gps[0],gps[1], precision = 10)
    if len(tempdata):
        db.updateDevice(id, data=tempdata)


def decode_file(deviceId, thread, batch, path):
    with open(path, "rb") as f:
        # path = path.replace("encoded","decoded")
        data = f.read()
        ser = jfw.deserializer(data, len(data))
        ser.search()
        hpd = None
        npd = None
        lpd = None
        vlpd = None
        info = None
        while(ser.decode_idx < len(ser.sync_char_off)):
            final_json = ser.decode(False)
            if(final_json != None):
                temp = json.loads(final_json)
                if 'hpd' in temp:
                    hpd = temp['hpd']
                if 'npd' in temp:
                    npd = temp['npd']
                if 'lpd' in temp:
                    lpd = temp['lpd']
                if 'vlpd' in temp:
                    vlpd = temp['vlpd']
                if 'async' in temp:
                    temp['async']['batteryId'] = "".join(chr(i) for i in temp['async']['batteryId'])
                    info = temp['async']
                    print(temp['async'])
                try:
                    item = thread(deviceId, temp['vhpd']['epoch'],
                    vhpd_data   =   temp['vhpd']['imuAxes'],
                    hpd_data    =   hpd,
                    npd_data    =   npd,
                    lpd_data    =   lpd,
                    vlpd_data   =   vlpd,
                    async_data  =   info)
                    data = None
                    data = batch.save(item)
                    time.sleep(0.065)
                except Exception as e:
                    log.debug(str(e))
                    print(e)
                    pass
        print(ser.loss())

def decode_and_push_data(Thread,batch, filter_devices):
    print("Listing Files")
    try:
        files = glob.glob("/var/data/*.bin", recursive=True)
        print(files)
        for filepath in files:
            filename = filepath.split("data/")[1]
            print(filename)
            print(filepath)
            temp = filename.split(".")[0].split("-")
            deviceId = temp[0]+"-"+temp[1]+"-"+temp[2]
            fileLastModified = os.path.getmtime(filepath)
            if(time.time() - fileLastModified > (60*60*3)):
                if deviceId in filter_devices:
                    decode_file(deviceId, Thread, batch, filepath)
                else:
                    print("Decoding Via New Method")
                    NewProcess = guru_decode.ProcessRawData(filepath)
                    NewProcess.decodeAndUpload(filepath)
                shutil.move(filepath, "/var/backup/"+filename)
            else:
                print("File too new to be processed!")
    except Exception as e:
        log.debug(str(e))
        print(e)

class Thread(Model):
    class Meta:
        table_name = os.environ["TABLE_NAME"]
        aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        # Specifies the region
        region = os.environ["AWS_REGION"]
    device_id       =   UnicodeAttribute(hash_key=True)
    timestamp       =   NumberAttribute(range_key=True)
    vhpd_data       =   JSONAttribute(null=True)
    hpd_data        =   JSONAttribute(null=True)
    npd_data        =   JSONAttribute(null=True)
    lpd_data        =   JSONAttribute(null=True)
    vlpd_data       =   JSONAttribute(null=True)
    async_data      =   JSONAttribute(null=True)

try:
    # Thread.delete_table()
    # time.sleep(5)
    filter_devices = []
    with open(os.path.join(os.path.dirname(__file__),"Deserializer/filter_device.json"), 'r') as filter_file:
        file_data = filter_file.read()
        temp_json_data = json.loads(file_data)
        filter_devices = temp_json_data["filtered_devices"]
    # aws_things = iot.deviceShawdow('LioBatteries')
    # db = firebase_db.rtdb()
    # db.connect()
    # things = aws_things.getThingList()
    log = logging.getLogger(__file__)
    log.setLevel(logging.DEBUG)
    try:
        if os.path.exists("/var/logs.txt"):
            os.remove("/var/logs.txt")
    except:
        pass
    handler = RotatingFileHandler("/var/logs.txt", maxBytes=5*1024*1024, backupCount=1)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(lineno)d - %(message)s')
    handler.setFormatter(formatter)
    # add the file handler to the logger
    log.addHandler(handler)
    empty = 0
    while True:
        if not os.listdir('/var/data') and (empty == 0):
            log.debug("Directory is empty")
            print("Directory is empty")
            empty = 1
        else:
            empty = 0
            if not Thread.exists():
                Thread.create_table(read_capacity_units=5, write_capacity_units=25, wait=True)
                print("Table Created")
                log.debug("Table Created")
            try:
                with Thread.batch_write(auto_commit=True) as  batch:
                    decode_and_push_data(Thread,batch, filter_devices)
                    log.debug("Saved")
                    print("Saved")
            except Exception as e:
                log.debug(str(e))
                print(str(e))
                pass
        # for items in things:
        #     aws_things.getDeviceShadow(items, callback=partial(customCallback,id=items))
        #     time.sleep(1)
        time.sleep(1*60)
except Exception as e:
    log.debug("Exiting Code :"+str(e))
    print(str(e))
    print("!!!!!!! Exiting Code !!!!!!!")
    pass

