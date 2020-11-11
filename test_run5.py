# coding=utf-8
import re
import time

import serial


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
        ser = serial.Serial('COM5', '115200', timeout=1)
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
        with open('FK20.gcode', 'r') as gcode_file:
            # 清空输入缓存区和输出缓存区
            ser.flushInput()
            num2 = 0
            num3 = 0
            total_data = ''
            while True:
                data = gcode_file.readline()
                data = judge_data(data=data)  # 处理命令中的注释与空行
                if data:
                    num2 += 1
                    total_data += data
                    if num2 >= 10:
                        send_size = ser.write(total_data.encode())
                        print("发送的数据{},发送的总行数{},发送的数据量{},输入缓存区{}".format(total_data, num2, send_size,ser.inWaiting()))
                        read_interval = 0.1
                        while True:
                            time.sleep(read_interval)
                            recv_data = ser.read_all().decode()
                            if recv_data.find('T') != -1:
                                read_interval = 3
                            matches = re.findall(r'ok', recv_data)
                            num3 += len(matches)
                            print("****返回的数据{}, 返回的ok数量{}，发送的总行数{}****".format(recv_data, num3, num2))
                            if num3 >= num2:
                                print("****返回的ok数量{}，发送的总行数{}****".format(num3, num2))
                                num2 = 0
                                num3 = 0
                                total_data = ''
                                break
                elif data == ";End of Gcode":
                    break
                # time.sleep(0.3)
    except Exception as e:
        print("打开串口错误{}".format(e))


if __name__ == '__main__':
    run()
