import time
import thread

class Indio:
    
    CHANNELS_PER_DEVICE = 12
    
    SERVO_H = 0
    SERVO_V = 1
    
    # No Args, sends all servos on device to home posiiton. 
    CMD_GO_HOME = 0x22 
    # Arg is pulsewidth in 1/4 us. Sending 0 turns off Servo. 6000 is about middle.
    CMD_SET_TARGET = 0x04 
    # Arg is units of (0.25 us)/(10 ms). Setting to 0 means unlimited.    
    CMD_SET_SPEED = 0x07 
    # Arg is acceleration limit, a value from 0 to 255 in units of (0.25 us)/(10 ms)/(80 ms). Setting 0 means no limit    
    CMD_SET_ACCEL = 0x09 
    
    BOTTOM = 0
    TOP = 254
    LEFT = 254
    RIGHT = 0
    
    DEFAULT_SPEED = 0
    DEFAULT_ACCEL = 0
    
    # num is the number of he indio (0-N)
    def __init__(self,pololu,device,num,offset_top = 0, offset_bottom = 0, offset_left = 0, offset_right = 0):
        self.__pololu = pololu
        self.__device = device
        self.__num = num
        self.__top = Indio.TOP - offset_top
        self.__bottom = Indio.BOTTOM + offset_bottom
        self.__left = Indio.LEFT - offset_left
        self.__right = Indio.RIGHT + offset_right
        self.__center = (self.__left - self.__right) / 2
        self.__cur_v_speed = Indio.DEFAULT_SPEED
        self.__cur_h_speed = Indio.DEFAULT_SPEED
        self.__cur_v_accel = Indio.DEFAULT_ACCEL
        self.__cur_h_accel = Indio.DEFAULT_ACCEL
        self.__reset()
    
    def __reset(self):
	    self.set_v_speed(Indio.DEFAULT_SPEED)
	    self.set_h_speed(Indio.DEFAULT_SPEED)
	    self.set_v_accel(Indio.DEFAULT_ACCEL)
	    self.set_h_accel(Indio.DEFAULT_ACCEL)
	    self.__send_command(Indio.CMD_GO_HOME)
    
    def __send_command(self,cmd,servo = -1,data1 = -1, data2 = -1):
        # start byte | device_id | command | servo_num | data1 | data2
        packet=chr(0xAA)+chr(self.__device)+chr(cmd)
        if servo > -1:
            packet = packet + chr(self.__num * 2 + servo)
        if data1 > -1:
            packet = packet + chr(data1)
        if data2 > -1:
            packet = packet + chr(data2)
        self.__pololu.send_cmd(packet)
   
    def go_home(self):
        packet=chr(0xAA)+chr(self.__device)+chr(cmd)
        self.__pololu.send_cmd(packet)
       
    
    def move_v(self,pos,speed, accel):
        if pos <0 or pos > 254:
            raise RuntimeError("Pos must be 0-255, you specified", pos)
        if self.__cur_v_speed != speed:
            self.set_v_speed(speed)
        if self.__cur_v_accel != accel:
            self.set_v_accel(accel)
        # Use mini SSC protocol since we just want 0-255 range, not specified in pulse widths
        packet=chr(0xFF)+chr((self.__device * Indio.CHANNELS_PER_DEVICE) + self.__num * 2 + Indio.SERVO_V)+chr(pos)
        self.__pololu.send_cmd(packet)
        
    
    def move_h(self,pos,speed, accel):
        if pos <0 or pos > 254:
            raise RuntimeError("Pos must be 0-255")
        if self.__cur_h_speed != speed:
            self.set_h_speed(speed)
        if self.__cur_h_accel != accel:
            self.set_h_accel(accel)
        # Use mini SSC protocol since we just want 0-255 range, not specified in pulse widths
        packet=chr(0xFF)+chr((self.__device * Indio.CHANNELS_PER_DEVICE) + self.__num * 2 + Indio.SERVO_H)+chr(pos)
        self.__pololu.send_cmd(packet)
    
    def set_v_speed(self,speed):
        if speed <0 or speed > 255:
            raise RuntimeError("Speed must be 0-255")
        self.__send_command(Indio.CMD_SET_SPEED, Indio.SERVO_V, speed & 0x7F,(speed & 0x80) >> 7)
        self.__cur_v_speed = speed
    
    def set_h_speed(self,speed):
        if speed <0 or speed > 255:
            raise RuntimeError("Speed must be 0-255")
        self.__send_command(Indio.CMD_SET_SPEED, Indio.SERVO_H, speed & 0x7F, (speed & 0x80) >> 7)
        self.__cur_h_speed = speed

    def set_v_accel(self,accel):
        if accel <0 or accel > 255:
            raise RuntimeError("Accel must be 0-255")
        self.__send_command(Indio.CMD_SET_ACCEL, Indio.SERVO_V , accel & 0x7F, (accel >> 7) & 0x7F)
        self.__cur_v_accel = accel

    def set_h_accel(self,accel):
        if accel <0 or accel > 255:
            raise RuntimeError("Accel must be 0-255")
        self.__send_command(Indio.CMD_SET_ACCEL, Indio.SERVO_H, accel & 0x7F, (accel >> 7) & 0x7F)
        self.__cur_h_accel = accel

        
    
    # Indio sits down
    def sit(self, offset = 0, speed = DEFAULT_SPEED, accel = DEFAULT_ACCEL):
        self.move_v(self.__bottom + offset, speed, accel)
    
    # Indio stand completely
    def stand(self, offset = 0, speed = DEFAULT_SPEED, accel = DEFAULT_ACCEL):
        self.move_v(self.__top - offset, speed, accel)
    
    # Indio center
    def center(self, offset = 0,speed = DEFAULT_SPEED, accel = DEFAULT_ACCEL):
	    self.move_h(self.__center - offset, speed, accel)
    
    # Indio all the way left
    def left(self, offset = 0, speed = DEFAULT_SPEED, accel = DEFAULT_ACCEL):
        self.move_h(self.__left - offset, speed, accel)
    
    # Indio all the way right
    def right(self, offset = 0, speed = DEFAULT_SPEED, accel = DEFAULT_ACCEL):
        self.move_h(self.__right + offset, speed, accel)

    def __side_shake(self, times):
        self.center()
        for x in range(0, times):
            self.center(-8,50)
            time.sleep(.1)
            self.center(8,50)
            time.sleep(.1)            
        self.center()
    
    def __dick_shake(self, times):
	    self.stand()
	    for x in range(0, times):
	        self.stand(20)
	        time.sleep(.1)
	        self.stand(60)
	        time.sleep(.1)
	        self.stand()
    
    def dick_shake(self,times, wait = False):
        if wait:
            self.__dick_shake(times)
        else:
           thread.start_new_thread( self.__dick_shake, (times,))


    def side_shake(self, times, wait = False):
        if wait:
            self.__side_shake(times)
        else:
            thread.start_new_thread( self.__side_shake, (times,))
    


