# coding=utf-8
import serial
import time
list = [
'M110 N0\n',
'G28\n',
'G1 X79.298 Y108.567 E0.07245\n'
]
# def test1():
#     try:
#         ser = serial.Serial('COM5', '115200', timeout=1)
#         if not ser.is_open:
#             ser.open()
#         with open('FK20.gcode', 'r') as gcode_file:
#             ser.flushInput()  # Flush startup text in serial input
#             ser.flushOutput()
#             print("00",ser.read_all().decode())
#             while True:
#                 data = gcode_file.readline()
#                 if not data.startswith(";"):
#                     print("发送的数据".format(data), "输入缓存区{}".format(ser.inWaiting()))
#                     ser.write(data.encode())
#                     ser.flush()
#                     res = ser.read_all()
#                     # res = ser.read('ok\n')
#                     # res = ser.readline()
#                     print(res.decode())
#                 elif data.startswith(";End of Gcode"):
#                     break
#                 time.sleep(0.1)
#     except Exception as e:
#         print("打开串口错误{}".format(e))

if __name__ == '__main__':
    test1()