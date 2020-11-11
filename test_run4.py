# coding=utf-8
import serial
import time
import threading
import re


#
# def recv_run(ser, event):
#     # 接收数据的子线程，通过event保持数据同步
#     num = 0
#     while True:
#         res = ser.read_all().decode()
#         matches = re.findall(r'ok', res)
#         num += len(matches)
#         if num == 3:
#             print("去输入缓存区读取的数据, 数量是", res, num)
#             event.set()
#             num = 0
#         else:
#             event.clear()
#         time.sleep(0.3)


def judge_data(data):
    if data.startswith(';End of Gcode'):
        return data
    if not data.startswith(';') and not data.startswith('\n'):
        if data.find(';') != -1:
            res = re.match('([A-Z].*);.*', data)
            line_data = res.group(1).strip() + '\n'
        else:
            line_data = data
    else:
        line_data = None
    return line_data


def run():
    try:
        ser = serial.Serial('COM4', '115200', timeout=1)
        if not ser.is_open:
            ser.open()
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

        with open('FK20.gcode', 'r') as gcode_file:
            # 清空输入缓存区和输出缓存区
            ser.flushInput()
            num2 = 0  # 记录发送了几行gcode命令
            num3 = 0  # 记录收到了几个ok
            total_data = ''
            first_send_signal = True
            while True:
                data = gcode_file.readline()
                data = judge_data(data=data)  # 处理命令中的注释与空行
                if data:
                    num2 += 1
                    total_data += data
                    if first_send_signal is True:
                        if num2 >= 10:
                            # 第一次写入打印机的数量
                            byte_total_data = total_data.encode()
                            send_size = ser.write(byte_total_data)
                            print("第一次发送的数据{}".format(byte_total_data), "第一次输入缓存区{}".format(ser.inWaiting()))
                            print("第一次发送的数据大小", send_size)
                            read_interval = 2
                            while True:
                                # time.sleep(read_interval)
                                recv_data = ser.read_all().decode()
                                print("------每次去缓存区取得数据", recv_data)
                                matches = re.findall(r'ok', recv_data)
                                num3 += len(matches)
                                if num3 >= 5:
                                    print("拿到的ok数", num3)
                                    first_send_signal = False
                                    num2 = 0
                                    total_data = ''
                                    break
                    else:
                        if num2 >= num3:
                            # 从第二次开始写入打印机的数量
                            byte_total_data = total_data.encode()
                            send_size = ser.write(byte_total_data)
                            print("******发送的数据", byte_total_data, "num2:", num2, "num3:", num3,
                                  "发送的数据大小", send_size,
                                  )
                            read_interval = 2
                            num4 = 0
                            while True:
                                # time.sleep(read_interval)
                                recv_data = ser.read_all().decode()
                                print("++++++每次去缓存区取得数据", recv_data)
                                matches = re.findall(r'ok', recv_data)
                                num4 += len(matches)
                                if num4 >= num2:
                                    print("拿到的ok数{}, num2:{}, num3:{}******".format(num4, num2, num3))
                                    num2 = 0
                                    total_data = ''
                                    break
                elif data == ";End of Gcode":
                    break
                # time.sleep(0.3)
    except Exception as e:
        print("打开串口错误{}".format(e))


if __name__ == '__main__':
    run()
