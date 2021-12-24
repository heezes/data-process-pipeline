from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute, JSONAttribute
from pathlib import Path
import jfwEncoderDecoder.jfw_deserializer as jfw
import json
import os
import time
import glob
import time
import shutil

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
                    print(e)
                    pass
        print(ser.loss())

def decode_and_push_data(Thread,batch):
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
            if(time.time() - fileLastModified > (60*60*2)):
                decode_file(deviceId, Thread, batch, filepath)
                shutil.move(filepath, "/var/backup/"+filename)
            else:
                print("File too new to be processed!")
    except Exception as e:
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
    while True:
        if not os.listdir('/var/data'):
            print("Directory is empty")
        else:
            if not Thread.exists():
                Thread.create_table(read_capacity_units=5, write_capacity_units=25, wait=True)
                print("Table Created")
            with Thread.batch_write(auto_commit=True) as  batch:
                decode_and_push_data(Thread,batch)
                print("Saved")
        time.sleep(15*60)
except:
    pass
