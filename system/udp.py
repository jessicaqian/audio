import socket #socket通信
import json #文件收发格式
import configparser #configparser用于读取web.ini文件


config = configparser.ConfigParser()
config.read("web.ini")
ip = config.get("systeminfo", "audioip")


def senddata(data):
    udp_send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    jsondata = json.dumps(data)
    udp_send.sendto(jsondata.encode('gbk'),(ip,8666))

    udp_send.close()



def heartbeat():
    udp_send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = {"msg_type":"AudioPing","seq":1}
    jsondata = json.dumps(data)
    udp_send.sendto(jsondata.encode('gbk'),(ip,8707)) #发送心跳命令给录音板

    udp_send.close()

