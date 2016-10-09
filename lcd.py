
import serial
import struct

CMD_CMD        = 0xFE
CMD_CLEAR      = 0x01
CMD_INVERT     = 0x12
CMD_ON         = 0x0C
CMD_OFF        = 0x08
CMD_BOX_CUR_ON = 0x0D
CMD_BOX_CUR_OFF= 0x0C
CMD_UND_CUR_ON = 0x0E
CMD_UND_CUR_OFF= 0x0C
CMD_MOV_CUR_R  = 0x14
CMD_MOV_CUR_L  = 0x10
CMD_SCRL_R     = 0x1C
CMD_SCRL_L     = 0x18
CMD_SET_CUR_POS= 0x80


CONFIG_CONFIG  = 0x7C

class Lcd(object):
  def __init__(self, port, baud):
    self.serial = serial.Serial(port=port, baudrate=baud)
    self.reset()
    
  def clear(self):
    self.command(CMD_CLEAR)

  def command(self, cmd, val=None):
    if val:
      cmd_str = struct.pack("BBB", CMD_CMD, cmd, val)
    else:
      cmd_str = struct.pack("BB", CMD_CMD, cmd)
    self.serial.write(cmd_str)

  def config(self, val):
    cmd_str = struct.pack("BB", CONFIG_CONFIG, val)
    self.serial.write(cmd_str)

  def write(self, string):
    self.serial.write(bytes(string, 'UTF-8'))

  def invert(self):
    self.command(CMD_INVERT)
  
  def brightness(self, val):
    #Val should be between 0.0 and 1.0
    if val < 0 or val > 1:
      return
    max = 157.0
    min = 128.0
    sval = (max-min)*val + min
    sval = int(round(sval))
    if sval < min or sval > max:
      return
    self.brightval = val 
    self.config(sval)
  
  def brighten(self):
    self.brightness(self.brightval*1.1)
  def darken(self):
    self.brightness(self.brightval*0.9)
  def on(self):
    self.command(CMD_ON)
  def off(self):
    self.command(CMD_OFF)
  def reset(self):
    self.clear()
    self.brightness(1.0)
    self.on()
  def box_cursor(self, state=True):
    if state:
      self.command(CMD_BOX_CUR_ON)
    else:
      self.command(CMD_BOX_CUR_OFF)
  def underline_cursor(self, state=True):
    if state:
      self.command(CMD_UND_CUR_ON)
    else:
      self.command(CMD_UND_CUR_OFF)
  def cursor_left(self):
    self.command(CMD_MOV_CUR_L)
  def cursor_right(self):
    self.command(CMD_MOV_CUR_R)
  def scroll_left(self):
    self.command(CMD_SCRL_L)
  def scroll_right(self):
    self.command(CMD_SCRL_R)
  def set_cursor_pos(self, x, y):
    pos = x
    if y == 1:
      pos += 64
    self.command(CMD_SET_CUR_POS | pos)
