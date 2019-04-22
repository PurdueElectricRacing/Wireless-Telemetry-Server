import websocket
import json
import datetime as dt
import logging
from datetime import datetime
import os
import random


def mc_parse_A5(can_id, data, time_pi):
    return {
        'id': can_id,
        'angle': int(data[:4], 16),
        'speed': int(data[4:8], 16),
        'e_out_freq': int(data[8:10], 16),
        'delta': int(data[10:12], 16),
        'parsed': True,
        'timestamp': time_pi
    }


def mc_parse_A8(can_id, data, time_pi):
    return {
        'id': can_id,
        'flux_command': int(data[:4], 16),
        'est_flux': int(data[4:8], 16),
        'id_fdbk': int(data[8:10], 16),
        'iq_fdbk': int(data[10:12], 16),
        'parsed': True,
        'timestamp': time_pi
        }


def mc_parse_AC(can_id, data, time_pi):
    fdbk = int(data[4:8], 16)

    # Feedback torque is sometimes negative
    if fdbk > 65535 * 0.9:
        fdbk -= 65535

    return {
        'id': can_id,
        'cmd_torque': int(data[:4], 16),
        'fdbk_torque': fdbk,
        'parsed': True,
        'timestamp': time_pi
    }


def mc_parse_AD(can_id, data, time_pi):
    return {
        'id': can_id,
        'mod_indx': int(data[:4], 16),
        'flx_weak': int(data[4:8], 16),
        'id_cmd': int(data[8:10], 16),
        'iq_cmd': int(data[10:12], 16),
        'parsed': True,
        'timestamp': time_pi
    }


def pedalbox2_parse(can_id, data, time_pi):
    return {
        'id': can_id,
        'throttle_1': int(data[:4], 16)* random.random(),
        'throttle_2': int(data[4:8], 16),
        'brake_1': int(data[8:12], 16) * random.random(),
        'brake_2': int(data[12:16], 16),
        'fancy': int(data[12:16], 16) * random.random(),
        'parsed': True,
        'timestamp': time_pi
    }


def pedalbox1_parse(can_id, data, time_pi):
    return {
        'id': can_id,
        'throttle_value': int(data[:4], 16),
        'brake_value': int(data[4:8], 16),
        'parsed': True,
        'timestamp': time_pi
    }


def no_parse_function_found(can_id, data, time_pi):
    # print("No parse function found for " + str(can_id) + " with data: " +
    #       str(data))
    return {'id': can_id, 'data': data, 'parsed': False}


def parse_CAN_frame(can_id, data, time):
    id_parse_functions = {
        '500': pedalbox1_parse,
        '501': pedalbox2_parse,
        '0A5': mc_parse_A5,
        '0A8': mc_parse_A8,
        '0AC': mc_parse_AC,
        '0AD': mc_parse_AD,
    }

    parse_function = id_parse_functions.get(
        can_id,
        no_parse_function_found)
    return parse_function(can_id, data, time)


class CANWebsocketClient():
    def __init__(self, callback, on_close, debug=False):
        self.callback = callback
        self.on_close = on_close
        self.is_debug = debug
        self.ws = None

    def on_message(self, message):
        data = json.loads(message)

        # When running from localhost, messages are sent in strings,
        # not JSON objects. They need to be parsed yet again...
        if self.is_debug and isinstance(data, str):
            data = json.loads(data)
            if 't' not in data:
                return

        # If type is data
        if data['t'] == 'd':
            payload = data['p']
            self.onRecvData(payload)

    def sendCANMEssage(self, m_id, message):
        message_len = str(len(message) / 2)
        message_fmt = 't' + m_id + message_len + message
        print("Sending message:", message_fmt)

        # self.ws.send(message)

    def onRecvData(self, payload):
        self.callback(payload)

    def on_error(self, ws, error):
        print(error)

    def start(self, address):
        if self.ws is not None:
            self.ws.close()
            self.ws = None

        self.ws = websocket.WebSocketApp(address,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def parseRawMessage(self, message, time):
        can_frame_data = parse_CAN_frame(
            message['i'],
            message['m'], time)

        return can_frame_data
