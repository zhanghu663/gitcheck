# coding=utf-8
import threading
import serial
import time
import re

event = threading.Event()


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


def send_data(ser):
        with open('FK20.gcode', 'r') as gcode_file:
            num2 = 0  # 记录发送了几行gcode命令
            while True:
                event.wait()
                data = gcode_file.readline()
                total_data = judge_data(data=data)  # 处理命令中的注释与空行
                if data and data != ";End of Gcode":
                    # 清空输入缓存区和输出缓存区
                    # total_data = ''
                    # num2 += 1
                    # total_data += data
                    # 写入打印机的数量
                    byte_total_data = total_data.encode()
                    send_size = ser.write(byte_total_data)
                    print("发送的数据{}".format(byte_total_data), "发送的数据大小", send_size)
                elif data == ";End of Gcode":
                    return


def recv_data(ser):
    read_interval = 2
    time.sleep(read_interval)
    ok_sum = 0
    while True:
        # recv_data = ser.read_all().decode()
        recv_data = ser.readline().decode()
        print("------每次去缓存区取得数据{}------".format(recv_data))
        matches = re.findall(r'ok', recv_data)
        ok_num = len(matches)
        ok_sum += ok_num
        if ok_num:
            event.set()
            print("拿到的ok数", ok_num)
        else:
            event.clear()


def main_run():
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
    except Exception as e:
        print("打开串口错误{}".format(e))
    else:
        thread1 = threading.Thread(target=send_data, args=(ser,))
        thread2 = threading.Thread(target=recv_data, args=(ser,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        print("运行完成")


if __name__ == '__main__':
    main_run()
