# For use with
# https://www.skpang.co.uk/collections/hats/products/raspberry-pi-pico-lin-bus-board
# RGB LIN-BUS LED
# https://www.skpang.co.uk/collections/breakout-boards/products/ncv7430-lin-bus-rgb-led-breakout-baord



from machine import UART, Pin
import time

SET_LED_CONTROL = 0x23
SET_LED_COLOUR  = 0x24

led = Pin(25, Pin.OUT)
led.value(1)

cs  = Pin(19, Pin.OUT)
wake  = Pin(18, Pin.OUT)

cs.value(1)
wake.value(1)
uart0 = UART(0, baudrate=19200, tx=Pin(16), rx=Pin(17))

def lin_parity(lin_id):
    bit = lambda v,b: (v>>b) & 0x1

    p0 = bit(lin_id ,0) ^ bit(lin_id,1)^ bit(lin_id ,2) ^ bit(lin_id ,4)
    p1 = 1^(bit(lin_id,1) ^ bit(lin_id ,3)^ bit(lin_id,4) ^ bit(lin_id,5))
    return (p0 | (p1<<1))<<6
    
def lin_write(lin_id,data,len,enhanced_crc):

    crc = calculate_crc(lin_id,data,len,enhanced_crc)
    lin_id = lin_id | lin_parity(lin_id)
  
    uart0.sendbreak()
    uart0.write(b'\x55')
    uart0.write(lin_id.to_bytes(1,'big'))
    uart0.write(data)
    uart0.write(crc.to_bytes(1,'big'))

def lin_read(data,len):
    time.sleep(1)
    
def calculate_crc(lin_id,array_bin, size, enhanced_crc):
            
    if enhanced_crc == 1:
        sum = lin_id
    else:
        sum = 0
    
    for i in range(size):
        sum = sum + array_bin[i]
            
        if sum >= 256:
              sum = sum-255
    sum = (-sum-1) & 0xff
    return sum

print("Raspberry Pi Pico LIN-bus NCV7430 RGB LED demo. skpang.co.uk 2023")

lin_init = bytearray([0xc0, 0x00, 0x00, 0x7f]) # Initialise NCV7430
lin_write(SET_LED_CONTROL,lin_init,4,0)
time.sleep(0.1)
    
    
while 1:
   
    led.value(1)
    set_red = bytearray([0xc0,0,0,0,0x31,00,0xff,0])
    lin_write(SET_LED_COLOUR,set_red,8,0)
    
    time.sleep(0.5)
    
    set_green = bytearray([0xc0,0,0,0,0x31,0xff,0,0])
    lin_write(SET_LED_COLOUR,set_green,8,0)
    time.sleep(0.5)
     
    set_blue = bytearray([0xc0,0,0,0,0x31,00,0,0xff])
    lin_write(SET_LED_COLOUR,set_blue,8,0)
    time.sleep(0.5)
    
    led.value(0)
    time.sleep(0.5)

