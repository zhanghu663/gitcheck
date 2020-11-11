
import re
import serial
import time
import serial.tools.list_ports

from NewPrinterBrain.settings import BAUDRATE_LIST


class SerialConfig(object):

    def get_port(self) -> list:
        """
        获取串口列表
        """
        serial_lists = list(serial.tools.list_ports.comports())  # 获取串口列表
        port_list = []
        if len(serial_lists) > 0:
            for i in serial_lists:
                device_port = i.device
                port_list.append(device_port)
        return port_list

    def check_port(self, port_list: list) -> list:
        """
        检查有效的串口列表
        """
        if port_list:
            for port in port_list:
                match_res = re.match('^/dev/ttyUSB.*', port)  # 正则匹配打印机是否以ttyUSB开头,若不是则从列表中删除
                if not match_res:
                    port_list.remove(port)
        return port_list

    def get_baudrate(self):
        """
        返回波特率列表
        @return:
        """
        return BAUDRATE_LIST


class PrinterSerial(serial.Serial):
    def __init__(self, serial_port, serial_baudrate, serial_timeout):
        super(PrinterSerial, self).__init__(port=serial_port, baudrate=serial_baudrate, timeout=serial_timeout)



if __name__ == '__main__':
    test_serial = SerialConfig()
    res = test_serial.get_port()
    res2 = test_serial.check_port(res)
    print(res2)
