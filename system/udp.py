import socket
import json
def senddata(data):
    udp_send = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    jsondata = json.dumps(data)
    udp_send.sendto(jsondata.encode('gbk'),("10.25.16.177",8666))
    udp_send.close()

def getdata(info):
    udp_get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_get.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 我们有时则需要一种超时机制使其在一定时间后返回而不管是否有数据到来，这里我们就会用到setsockopt()函数
    udp_get.bind(("0.0.0.0",8711))
    # 接收数据
    recv_data0 = udp_get.recvfrom(1024)  # 接收数据最大字节数   recv_data为一个元组(数据，发送方ip,端口)
    # recv_msg = recv_data[0]   #数据
    # recv_addr = recv_data[1]   #发送方的地址
    # print(recv_data,recv_msg.decode('gbk'),recv_addr)  #decode解码windows系统默认编码方式是gbk
    print(recv_data0[0].decode('gbk'))
    jsondata0 = recv_data0[0].decode('gbk')
    data0 = json.loads(jsondata0)
    if data0["audioFuncAck"]==info["audioPara"]["audioFunc"]:
        recv_data = udp_get.recvfrom(1024)
        print(recv_data[0].decode('gbk'))
        jsondata = recv_data[0].decode('gbk')
        data = json.loads(jsondata)
        if data["audioAckValue"]["audioFunc"]==info["audioPara"]["audioFunc"]:
            return data
        else:
            return False
    else:

        return False

