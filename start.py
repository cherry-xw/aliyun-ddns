import json, os, time
from urllib.request import urlopen
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import  DescribeDomainRecordsRequest, UpdateDomainRecordRequest

base_dir = os.path.dirname(os.path.realpath(__file__))
config_file_url = os.path.join(base_dir, 'config.json')
log_file_url = os.path.join(base_dir, 'config.log')
log_data = {}

try:
    log = open(log_file_url, 'a')
    log_data['time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

    data = open(config_file_url, 'r').read()
    config_json = json.loads(data)

    ID = config_json['AccessKeyID']
    Secret = config_json['AccessKeySecret']
    RegionId = config_json['RegionId']
    DomainName = config_json['DomainName']
    HostReacrd = [config_json['HostReacrd']]
    Types = config_json['Types']
    CurrentIP = config_json['CurrentIP']

    log_data['last_ip'] = CurrentIP

    clt = client.AcsClient(ID, Secret, RegionId)
except Exception as e:
    log_data['load_config_error'] = str(e)
    time.sleep(2)

def GetAllDomainRecords(DomainName, Types, IP):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)

    try:
        DomainRecordsJson = json.loads(clt.do_action_with_exception(DomainRecords))
        who_data = DomainRecordsJson['DomainRecords']['Record']
        log_data['record'] = who_data
        for HostName in HostReacrd:
            for x in who_data:
                RR = x['RR']
                Type = x['Type']
                if RR == HostName and Type == Types:
                    RecordId = x['RecordId']
                    EditDomainRecord(HostName, RecordId, Types, IP)
    except Exception as e:
        log_data['record_error'] = str(e)

def EditDomainRecord(HostName, RecordId, Types, IP):
    UpdateDomainRecord = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    UpdateDomainRecord.set_accept_format('json')
    UpdateDomainRecord.set_RecordId(RecordId)
    UpdateDomainRecord.set_RR(HostName)
    UpdateDomainRecord.set_Type(Types)
    UpdateDomainRecord.set_TTL('600')
    UpdateDomainRecord.set_Value(IP)
    try:
        UpdateDomainRecordJson = json.loads(clt.do_action_with_exception(UpdateDomainRecord))
        log_data['update'] = UpdateDomainRecordJson
    except Exception as e:
        log_data['update_error'] = str(e)

def main():
    text = urlopen("http://ip.taobao.com/service/getIpInfo.php?ip=myip").read()
    jsonStr = json.loads(text)
    IP = jsonStr["data"]["ip"]
    if (CurrentIP == IP):
        log_data['msg'] = '当前ip与上次记录ip相同，无需更新'
    else:
        log_data['ip'] = IP
        if (DomainName is not None and Types is not None):
            GetAllDomainRecords(DomainName, Types, IP)
            config_json['CurrentIP'] = IP
            open(config_file_url, 'w').write(json.dumps(config_json))
        else:
            log_data['msg'] = '请正确配置DomainName,Types'
    log.write(json.dumps(log_data) + '\n')
    time.sleep(2)

if __name__ == '__main__':
    main()