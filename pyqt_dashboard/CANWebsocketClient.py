import websocket
import json
import datetime as dt
import logging
from datetime import datetime
import os

def mc_parse_A5(can_id, data, time_pi):
     return {
        'id': can_id,
        'angle': int(data[:4], 16),
        'speed': int(data[4:8], 16) ,
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

    if fdbk > 65279 * 0.9:
        fdbk -= 65279
    
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
        'throttle_1': int(data[:4], 16),
        'throttle_2': int(data[4:8], 16),
        'brake_1': int(data[8:12], 16),
        'brake_2': int(data[12:16], 16),
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


def parseRawMessage(message, time):
    can_frame_data = parse_CAN_frame(
        message['id'],
        message['message'], time)

    # if can_frame_data['parsed']:
    return can_frame_data


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
            if 'type' not in data:
                return
        if data['type'] == 'data':
            payload = data['payload']
            self.onRecvData(payload)

    def onRecvData(self, payload):
        buffer = []
        for m_id in payload:
            buffer.append(payload[m_id])
        self.callback(buffer)

    def on_error(ws, error):
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
