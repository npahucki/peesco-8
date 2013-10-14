import serial
import pololu
import sys
import time

DEVICE_TYPE = 0x0C

CMD_SET_PARAMS = 0x00
CMD_SET_SPEED = 0x01
CMD_SET_POSITION = 0x02
CMD_SET_POSITION_EXT = 0x03
CMD_SET_POSITION_ABS = 0x04
CMD_SET_NEUTRAL = 0x05


ser=serial.Serial('/dev/cu.usbmodem00059921', 56000, timeout=1)
__pololu = pololu.Pololu(ser)

def __send_command(cmd,servo,data1, data2 = -1):
    # start byte | device_id | command | servo_num | data1 | data2
    packet=chr(0xAA)+chr(DEVICE_TYPE)+chr(cmd)+chr(servo)+chr(data1)
    if data2 > -1:
        packet = packet + chr(data2)
    __pololu.send_cmd(packet)

def move(servo, pos):
    __send_command(CMD_SET_POSITION_ABS, servo, (pos & 0x80) >> 7, pos & 0x7F)



n=int(sys.argv[1])
m=int(sys.argv[2])

move(n,m)
time.sleep(1)

