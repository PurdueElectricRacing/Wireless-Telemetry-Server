import sys
from SensorDict import CANParser
from collections import Counter 
import datetime as dt

parser = CANParser()

OUTPUT_SOURCE_FILE = "CANHelper.c"
OUTPUT_HEADER_FILE = "CANHelper.h"

# Given a list of names, find the common values across all of them
# Example:
#   ['PER is great', 'PERathon', 'PER is my fav']
# returns:
#   'PER'

def get_common_list(sensor_names):
    common = sensor_names[0]
    for i in range(1, len(sensor_names)):
        common = common_start(common, sensor_names[i])
    return common


def common_start(sa, sb):
    def _iter():
        for a, b in zip(sa, sb):
            if a == b:
                yield a
            else:
                return
    return ''.join(_iter())


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def get_c_int_datatype(bits):
    if bits == 8:
        return 'int8_t'
    elif bits == 16:
        return 'int16_t'
    elif bits == 24:
        return 'int32_t'
    elif bits == 32:
        return 'int32_t'
    elif bits == 1:
        return 'bool'
    else:
        return 'void'


# Display formatted text for either pasting into google sheets
# or on the wiki for reference.
if __name__ == '__main__':
    # Generate CANHelper.c for use in the main module/DAQ code
    # This file will be used for abstracting the CAN functions
    # away from the programmer.

    # INTENDED C CODE TO SEND MESSAGES:
    # sendRearWheelSpeed(speed_l, speed_r);
    source_file_source = ""
    all_function_headers = []

    # GENERATE SOURCE FILE
    source_file_source = """/* 
* Generated on {}
* This file creates a list of functions used to send
* CAN messages with abstracted IDs and messages.
*/

#include "CANHelper.h"

""".format(str(dt.datetime.now()))

    for dec_id, sensors in parser.sensorLib.items():
        sensor_names = [name for name in sensors]
        bits = [sensors[name] for name in sensors]

        params = [to_camel_case(name.lower()) for name in sensor_names]
        types = [get_c_int_datatype(bit_range[0] - bit_range[1] + 1) for bit_range in bits]

        common_name = get_common_list(sensor_names).lower()
        if common_name is "" or "flag" in common_name:
            continue
        function_name = to_camel_case("send_" + common_name)

        function_header = "void " + function_name + "(" + (', '.join([data_type + " " + param for data_type, param in zip(types, params)])) + ")"

        all_function_headers.append(function_header)

        id_string = common_name.rstrip("_").upper()
        function_body = "\tCanTxMsgTypeDef tx;\
                        \r\ttx.IDE = CAN_ID_STD;\
                        \r\ttx.RTR = CAN_RTR_DATA;\
                        \r\ttx.StdId = {};\
                        \r\ttx.DLC = 1;\n\n".format(id_string + "_CAN_ID")
        byte_num = 0
        for i, param in enumerate(params):
            data_size = bits[i][0] - bits[i][1] + 1
            data_line = "\ttx.Data[{}] = {} & 0xFF;\n".format(byte_num, param)
            byte_num += 1
            for extra_byte in range(1, int(data_size/8)):
                data_line += "\ttx.Data[{}] = {} >> {};\n".format(byte_num, param,  extra_byte * 8)
                byte_num += 1
            
            function_body += data_line + "\n"

        source_file_source += "\n // GENERATED FUCTION\n"
        source_file_source += function_header + "\n"
        source_file_source += "{\n"
        source_file_source += function_body
        source_file_source += "\txQueueSendToBack(car.q_tx_dcan, &tx, 100);\n"
        source_file_source += "}\n"

    save_file = open(OUTPUT_SOURCE_FILE, "w+")
    save_file.write(source_file_source)
    save_file.close()

    # GENERATE HEADER FILE
    header_file_source = """/* 
* Generated on {}
* This file creates a list of functions used to send
* CAN messages with abstracted IDs and messages.
*
*/

#include "CANProcess.h"
#include "CANID.h"

#ifndef CANHelper_H
#define CANHelper_H\n\n""".format(str(dt.datetime.now()))

    header_file_source += (";\n".join(all_function_headers)+";")

    header_file_source +="\n\n#endif"

    save_file = open(OUTPUT_HEADER_FILE, "w+")
    save_file.write(header_file_source)
    save_file.close()
