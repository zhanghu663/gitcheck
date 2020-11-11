import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from dwebsocket.decorators import accept_websocket
import time
import json
from NewPrinterBrain.settings import response_format, \
    CODE_2000, CODE_4003, MESSAGE_2000, MESSAGE_4003, READ_TIMEOUT, CODE_5000, MESSAGE_5000
from printer_center.models import SerialConfig, PrinterSerial

from printer_center.serial_util import judge_data

ser = None  # 定义全局变量serial实例
pause_status = False  # 定义暂停的状态，默认false
cancel_status = False  # 定义取消的状态，默认false
print_status = False  # 定义打印的状态，默认false

logger = logging.getLogger('django')


import time
@accept_websocket
def test2_websocket(request):
    num = 0
    while num < 600:
        time.sleep(1)
        request.websocket.send("receive printer data {}:".format(num))
        num += 1
    request.websocket.close()
    return

def test(request):
    # url http://ip:port/test/

    ipaddress = request.META['REMOTE_ADDR']
    print(ipaddress)
    a = 1+ 1
    b = 2+2
    c = 3+3
    print(c)
    print(a)
    print(b)
    return JsonResponse({"code":200, "ipaddress":ipaddress})


def get_serial_config(request):
    """
    获取串口及波特率列表
    url: http://ip:port/cxsw/serial/config/ get
    """
    printer_serial = SerialConfig()
    port_list = printer_serial.get_port()
    port_list = printer_serial.check_port(port_list)
    baudrate_list = printer_serial.get_baudrate()
    response = response_format(code=CODE_2000,
                               data=dict(port_list=port_list, baudrate_list=baudrate_list),
                               message=MESSAGE_2000
                               )
    return JsonResponse(response)


@require_POST
def get_connect(request):
    """
    与打印机建立连接
    url: http://ip:port/cxsw/printer/connect/ post
    :param request:
    :return:
    """
    request_data = json.loads(request.body)
    serial_port = request_data.get('serial_port', 'COM5')
    serial_baudrate = request_data.get('serial_baudrate', 115200)
    if not serial_port or not serial_baudrate:
        return JsonResponse(response_format(code=CODE_4003, data=None, message=MESSAGE_4003))
    try:
        printer_serial = PrinterSerial(serial_port, serial_baudrate, READ_TIMEOUT)
    except Exception as e:
        logger.error("串口打开失败:错误{}".format(e))
        return JsonResponse(response_format(code=CODE_5000, data=None, message=MESSAGE_5000))
    global ser
    ser = printer_serial
    if not ser:
        return JsonResponse(response_format(code=CODE_5000, data=None, message=MESSAGE_5000))
    global print_status
    print_status = True
    return JsonResponse(response_format(code=CODE_2000, data=None, message=MESSAGE_2000))





@accept_websocket
def test_websocket(request):
    print('1111')
    """
    打印并返回数据
    url：ws://127.0.0.1:8000/cxsw/printer/
    :param request:
    :return:
    """
    if request.is_websocket():
        if ser:
            # 和打印机进行hello world
            num1 = 0
            while True:
                time.sleep(0.2)
                data = ser.read_all().decode()
                if data.find('init valid') != -1:
                    num1 += 1
                    if num1 >= 1:
                        break
                elif num1 >= 3:
                    break
                num1 += 1

            with open('FKYZ.gcode', 'r') as gcode_file:
                # 清空输入缓存区和输出缓存区
                ser.flushInput()
                while True:
                    print(ser)
                    print(id(ser))
                    print("print_status:{},pause_status:{},cancel_status:{}".format(print_status, pause_status, cancel_status))
                    if print_status and not pause_status and not cancel_status:
                        command = gcode_file.readline()
                        str_command = judge_data(data=command)  # 处理命令中的注释与空行
                        if str_command and not str_command.startswith(";End of Gcode"):
                            bytes_command = str_command.encode()
                            size = ser.write(bytes_command)
                            print("------写入的数据{},写入的数据量{}".format(bytes_command, size))
                            num = 0  # 记录重发次数
                            while True:  # 循环读取数据
                                bytes_recv_data = ser.readline()
                                print("每次去缓存区取得数据{}-----".format(bytes_recv_data))
                                request.websocket.send(bytes_recv_data.decode())
                                if b'ok' in bytes_recv_data:
                                    break
                                elif bytes_recv_data == b'':
                                    if num >= 2:
                                        request.websocket.send("receive printer data error")
                                        logger.error("receive printer data error: {}".format(bytes_recv_data.decode()))
                                        request.websocket.close()
                                        return
                                    try:
                                        size = ser.write(bytes_command)
                                        num += 1
                                        logger.info("rewrite gcode:{}, size:{}".format(bytes_command, size))
                                    except Exception as e:
                                        request.websocket.send("rewrite gcode error")
                                        logger.error("rewrite gcode:{}, error: {}".format(bytes_command, e))
                                        request.websocket.close()
                        elif str_command and str_command.startswith(";End of Gcode"):
                            request.websocket.send("print finish")
                            logger.info("send gcode finish")
                            request.websocket.close()
                            return
                    elif not print_status and pause_status and not cancel_status:
                        # 暂停之后等
                        request.websocket.send("print pause")
                        logger.info("status:pause print")
                        time.sleep(2)
                    elif not print_status and not pause_status and cancel_status:
                        # 取消打印 M106 S0:关闭风扇, M104 S0：关闭喷嘴升温, M140 S0：关闭热床升温
                        cancel_command_list = ['M106 S0\n', 'M104 S0\n', 'M140 S0\n', 'M84\n']
                        for cancel_command in cancel_command_list:
                            ser.write(cancel_command.encode())
                            bytes_recv_data = ser.readline()
                            if b'ok' in bytes_recv_data:
                                logger.info("write cancel command {}".format(cancel_command))
                                continue
                        request.websocket.send("print cancel")
                        request.websocket.close()
                        logger.info("cancel finish")
                        # global print_status, pause_status, cancel_status
                        # print_status = True
                        # pause_status = False
                        # cancel_status = False
                        return
        else:
            request.websocket.send("serial error")
            request.websocket.close()
            return
    return JsonResponse(response_format(code=CODE_4003, data=None, message=MESSAGE_4003))


@require_POST
def change_printer_status(request):
    """
    对打印状态的标识符进行修改
    url http://ip:port/cxsw/printer/status/ post
    :param request:
    :return:
    """
    request_data = json.loads(request.body)
    print_command = request_data.get('command', None)
    global print_status, pause_status, cancel_status
    if print_command == 'print':
        print_status = True
        pause_status = False
        cancel_status = False
    if print_command == 'pause':
        print_status = False
        pause_status = True
        cancel_status = False
    elif print_command == 'cancel':
        print_status = False
        pause_status = False
        cancel_status = True
    return JsonResponse(response_format(code=CODE_2000, data=None, message=MESSAGE_2000))
