# coding=utf-8
import serial
import serial.tools.list_ports


class TestSerial(object):
    def __init__(self):
        pass

    def get_port(self):
        """
        获取有效的串口列表
        """
        serial_lists = list(serial.tools.list_ports.comports())
        port_list = []
        if len(serial_lists) > 0:
            for i in serial_lists:
                device_port = i.device
                port_list.append(device_port)
        return port_list

    def check_port(self, port_list: list):
        """
        检查哪个串口是打印机的
        """
        for port in port_list:
            try:
                ser = serial.Serial(port, '115200', timeout=0.5)
                if ser.isOpen():
                    print("ok")
                else:
                    ser.open()

                print(ser.name)
            except Exception as e:
                raise e
                # continue
            return ser


import serial
import time
list = [
'M110 N0\n',
'G28\n',
'G1 X79.298 Y108.567 E0.07245\n',
]
ser = serial.Serial('COM5', '115200', timeout=1)
print(ser.in_waiting)
for i in list:
    ser.write(i.encode())
    res = ser.read_all().decode()
    print(res)
    count2 = ser.inWaiting()
    res2 = ser.read(count2).decode()
    print(res2)
    # print(count)
    while True:
        ser.write('M115\n'.encode())
        ser.flush()
        recv_data = ser.read_all().decode()
        print(recv_data)
        if recv_data.find('FIRMWARE_NAME') != -1 and recv_data.find('UUID'):
            break
        time.sleep(0.2)


if __name__ == '__main__':
    pass
    # test_serial = TestSerial()
    # port_list = test_serial.get_port()
    # test_serial.check_port(port_list)
    # print(port_list)