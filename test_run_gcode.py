# coding=utf-8
import threading
import time
import chardet
import serial


def read_data(ser):
    while True:
        # res = ser.read()
        # print('aaa',res)
        num = ser.in_waiting
        print(num)
        if num > 0:
            data = ser.read_all().decode()
            print("有数据返回", data)
        else:
            print("没有数据返回")
        time.sleep(1)


def get_gcode_file():
    ser = serial.Serial('COM5', '115200', timeout=0.5)
    is_open = ser.is_open
    if is_open:
        # read_thread = threading.Thread(target=read_data, args=(ser,))
        # read_thread.start()
        pass
    else:
        ser.open()
    with open('test.gcode', 'r') as gcode_file:
        while True:
            data = gcode_file.readline()
            if not data.startswith(";"):
                write_size = ser.write(data.encode())
                recv_data = ser.readline()
                print('*' * 50)
                print("写入的字节数:{},写入的数据{}".format(write_size, data))
                print("读取的数据：{}".format(recv_data.decode()))
                print('*' * 50)
                with open('recv_data.txt', 'a') as recv_file:
                    recv_file.write("命令:{}, 返回的数据{}".format(data, recv_data.decode()))
                time.sleep(1)
            elif data.startswith(";End of Gcode"):
                break
    print("打印结束")


import time


def test_gcode_readline():
    ser = serial.Serial('COM5', '115200', timeout=20)
    is_open = ser.is_open
    if not is_open:
        ser.open()
    ser.flushInput()
    data = 'G28\n'
    write_size = ser.write(data.encode())
    print(write_size)
    while True:
        recv_data = ser.readline()
        if b'ok\n' in recv_data:
            print('1111')
            break
        print(recv_data, time.time())
        time.sleep(0.02)


if __name__ == '__main__':
    test_gcode_readline()
