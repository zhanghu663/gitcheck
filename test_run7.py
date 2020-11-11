# coding=utf-8
import serial
import time
import re

def data_checksum(command, linenumber):
    # command = 'G1 X48.638 Y40.36 E0.93237'
    # linenumber = 4
    if command.endswith('\n'):
        command = command.replace("\n", '')
    command = command.encode("ascii", errors="replace")
    command_to_send = b"N" + str(linenumber).encode("ascii") + b" " + command
    checksum = 0
    for c in bytearray(command_to_send):
        checksum ^= c
    command_to_send = command_to_send + b"*" + str(checksum).encode("ascii")
    command_to_send += b"\n"
    return command_to_send


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
        ser = serial.Serial('COM5', '115200', timeout=4)
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
            while True:
                command = gcode_file.readline()
                str_command = judge_data(data=command)  # 处理命令中的注释与空行
                if str_command and not str_command.startswith(";End of Gcode"):
                    bytes_command = str_command.encode()
                    result = ser.write(bytes_command)
                    print("------写入的数据{}-----写入的数据量{}-----".format(bytes_command, result))
                    num = 0 # 记录重发次数
                    while True:  # 循环读取数据
                        bytes_recv_data = ser.readline()
                        print("------每次去缓存区取得数据{}-----".format(bytes_recv_data))
                        if b'ok' in bytes_recv_data:
                            break
                        elif bytes_recv_data == b'':
                            if num >= 2:
                                return
                            try:
                                res = ser.write(bytes_command)
                                num += 1
                                print("------重新写入的数据{}-----写入的数据量{}-----".format(bytes_command, res))
                            except Exception as e:
                                print(e)
                                return
                elif str_command and str_command.startswith(";End of Gcode"):
                    break
    except Exception as e:
        print("打开串口错误{}".format(e))


if __name__ == '__main__':
    run()
