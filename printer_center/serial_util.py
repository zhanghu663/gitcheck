# coding=utf-8
import re


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