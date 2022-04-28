import os
import sys
import requests
import base64
import tarfile
import time
import PySimpleGUI as sg
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring
from requests import get
from requests.structures import CaseInsensitiveDict

REMOTESUPPORT_OUTPUT="./output"
REMOTESUPPORT_FOLDER="dropbox"
REMOTESUPPORT_SSLSNI="eid.18"
REMOTESUPPORT_MODULE_PA="pa"
URL_MODULE_NAME='ng1api/'
NCM_URL_MODULE_NAME=URL_MODULE_NAME+'ncm/'
XML_HEADER="""<?xml version="1.0"?>"""
REMOTEUPDATE_COMMAND="""<?xml version="1.0"?><Request>
<Commands Count="1">
<Command>
<Name>NOTIFY</Name>
<Arguments>
<Target>MASKING_FILE_SYNC</Target>
<FileName>IS_Decode_Protocols.xml</FileName>
<PMSync>true</PMSync>
</Arguments>
</Command>
</Commands>
</Request>"""


def upload_to_device(deviceListInfo,deviceCount):
    headers = {
    'Content-Type': 'application/binary',
    'User-Agent': 'Netscout_PUT',
    }
    for x in range(deviceCount):
        deviceInfo = deviceListInfo[x]
        create_url=deviceInfo[2] + "://"+ deviceInfo[0]+ ":"+deviceInfo[1]+"/"
        create_request_url = create_url + REMOTESUPPORT_FOLDER + "/"
        #create_request_url="http://172.22.24.62:8080/dropbox/temp.tar.gz"
        auth_string_temp = "rwcommunity:"+deviceInfo[2]+"@"+deviceInfo[3]
       # auth_string_temp = "rwcommunity:"+ "public"+"@"+"public"
        message_bytes = auth_string_temp.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        auth_string = base64_bytes.decode('ascii')
        auth_string = "Basic " + base64_bytes.decode('ascii')
        headers["Authorization"] = auth_string
        file_ext = os.path.splitext(transfer_file_name)
        if (file_ext[1] == ".gz" ): #file_ext[1] == ".pcap" or file_ext[1] == ".pcap" ):
            headers["Content-Type"]='application/x-gzip'
        elif (file_ext[1] == ".cfg" or file_ext[1] == ".txt" or file_ext[1] == ".ini" ):
            headers["Content-Type"]= 'text/plain'
        elif (file_ext[1] == ".xml" ):
             headers["Content-Type"]= 'application/xml'
        files = {'file':(transfer_file_name, open(transfer_file_name, 'rb'))}
        
      
        myxml = ET.fromstring(REMOTEUPDATE_COMMAND)
        myxml.find('./Commands/Command/Arguments/FileName').text=transfer_file_name
        xmlstr = ET.tostring(myxml)
        xmlstr = xmlstr.decode('UTF-8')
       
        
        create_transfer_url = create_request_url + transfer_file_name
        with open(transfer_file_name, 'rb') as data:
           r=requests.put(create_transfer_url,headers=headers,data=data,verify=False)
        if(r.status_code == 200 or r.status_code ==201):
           print("success")
           create_command_url=create_url + REMOTESUPPORT_MODULE_PA
           headers["Content-Type"]= 'text/xml'
           data= XML_HEADER + xmlstr
           rp =requests.post(create_command_url,data=data,headers=headers,verify=False)
           print (create_request_url)
        print (REMOTEUPDATE_COMMAND)


def device_list_handler(responseXml):
    deviceCount=0
    deviceListInfo = []
    responseXml.findall(".")
    #for x in range(len(responseXml.findall("./DeviceConfiguration"))):
    for DeviceConfigurations in responseXml.findall("./DeviceConfiguration"):
        DeviceType = DeviceConfigurations.findall("./DeviceType")
        if (DeviceType[0].text == 'vSTREAM' or DeviceType[0].text == 'InfiniStream'):
            deviceInfo = []
            DeviceConfig = DeviceConfigurations.findall("./DeviceConfiguration")
            DeviceIP = DeviceConfigurations.findall("./DeviceIPAddress")
            DeviceProtocol = DeviceConfigurations.findall("./CommunicationProtocol")
            DeviceReadString = DeviceConfigurations.findall("./ReadCommunityString")
            DeviceWriteString = DeviceConfigurations.findall(".WriteCommunityString")
            DevicePort = DeviceConfigurations.findall("./Port")
    
            #eviceInfo.insert(0,DeviceIP[0].text)
            deviceInfo.append(DeviceIP[0].text)
            if (len(DevicePort) == 0):
               deviceInfo.append('8443')
            else:
               deviceInfo.append(DevicePort[0].text)
                         
            deviceInfo.append(DeviceProtocol[0].text)
            deviceInfo.append(DeviceReadString[0].text)
            deviceInfo.append(DeviceWriteString[0].text)
            deviceListInfo.append(deviceInfo)

            deviceCount +=1
    upload_to_device(deviceListInfo,deviceCount)

#server list handler is currently dummy code , not fully implemented
def server_list_handler():
    url = 'https://172.20.170.55:8443/ng1api/ncm/servers'
    #response = requests.get(url, auth=('administrator', 'netscout1'),headers=headers, verify=False)
    response = sessionInfo.get(url, params=params, headers=headers, verify=False)
    responseXml = ET.fromstring(response.content)
    DeviceIP = responseXml.findall("./Server/ipAddress")
    DeviceProtocol = responseXml.findall("./Server/serverProtocol")
    DevicePort = responseXml.findall("./Server/httpPort")

def compress_files(file_list):
    global transfer_file_name
    seconds = time.time()
    seconds_string=str(seconds)
    temp_file_name = "archive_" + (seconds_string.split("."))[0] + (seconds_string.split("."))[1]
    file_names = file_list.split(',')
    transfer_file_name = temp_file_name + ".tar.gz"
    tar = tarfile.open(transfer_file_name, "w:gz")
    for x in range(len(file_names)):
        tar.add(file_names[x], os.path.basename(file_names[x]))
    tar.close
    

def main():
    #form = sg.FlexForm('Login')
    layout = [
          [sg.Text('Protocol',size=(10, 1)),sg.Combo(['http','https'],key='protocol')],
          [sg.Text('IP Address', size=(10, 1)), sg.InputText('')],
          [sg.Text('Port', size=(10, 1)), sg.InputText('')],
          [sg.Text('Name', size=(10, 1)), sg.InputText('')],
          [sg.Text('Password', size=(10, 1)), sg.InputText('', password_char='*')],
          [sg.Submit(), sg.Cancel()]
         ]

    cliLayout = [
          [sg.Text('Operation',size=(10, 1)),sg.Combo(['exportCLI',''],key='operation')],
          [sg.Text('Start Time', size=(10, 1)), sg.InputText('')],
          [sg.Text('End Time', size=(10, 1)), sg.InputText('')],
          [sg.Text('Filter', size=(50, 1)), sg.InputText('')],
          [sg.Text('Command Line Params', size=(20, 1)), sg.InputText('')],
          [sg.Submit(), sg.Cancel()]
         ]
    
    window = sg.Window('Login', layout)    
    #button, values = form.Layout(layout).Read()
    while True:             # Event Loop
       button, values = window.Read()
        # print(event, values)
       if button in (None, 'Cancel'):            # if exit button or closed using X
            break
       elif 'Submit' in button and (values[0] != "" and values[1] != "" and values[2] != "" and values[3] != ""):
            ConfigFile = open('config.txt', 'r')
            Lines = ConfigFile.readlines()
            ConfigFile.close()
            global file_list
            fields = Lines[0].split()
            server_protocol = fields[1]
            server_ip = values[0]#fields[2]
            server_port = values[1]#fields[3]
            server_username= values[2]#fields[4]
            server_pwd =values[3]#fields[5]
            file_list = fields[6]

            compress_files(file_list)

            # current implementation for single server configuration 
            server_base_url = server_protocol+"://"+server_ip+":"+server_port+"/"
            server_module_url = server_base_url+URL_MODULE_NAME

            sessionInfo = requests.Session() 
            rest_session_url = server_module_url+'rest-sessions'

            response = sessionInfo.post(rest_session_url, verify=False, auth=(server_username, server_pwd))
            print(response.text)
            window.Close() 
            if(response.text != '{}'):
                print("Connection not successful")
            cliWindow = sg.Window('Operation', cliLayout,finalize=True,modal=True)   
            button, values = window.Read()
            headers = {'content-type': 'application/xml'}
            params = (('include_privileges', 'true'),)
            device_list_url = server_base_url+NCM_URL_MODULE_NAME+'devices'
            #url = 'https://172.20.170.55:8443/ng1api/ncm/devices'
            #response = requests.get(url, auth=('administrator', 'netscout1'),headers=headers, verify=False)
            #cookies = response.content
            #response = s.get('https://172.20.170.55:8443/ng1api/ncm/users/administrator', params=params,  verify=False)
            response = sessionInfo.get(device_list_url, params=params, headers=headers, verify=False)
            responseXml = ET.fromstring(response.content)
            device_list_handler(responseXml)
            #server_list_handler()
            session_close_url = rest_session_url + '/close'
            sessionInfo.post(session_close_url, verify=False)
       else:
            break
    window.Close() 
    
   
    

if __name__ == "__main__":
    main()



