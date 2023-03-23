# For use with
# https://www.skpang.co.uk/collections/hats/products/raspberry-pi-pico-lin-bus-board

from machine import UART, Pin
import time

SLAVE_ADDRESS = 0x49   # Slave address of window swtich

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
    lin_id = lin_id | lin_parity(lin_id) # Add parity
  
    uart0.sendbreak()
    uart0.write(b'\x55')
    uart0.write(lin_id.to_bytes(1,'big'))
    uart0.write(data)
    uart0.write(crc.to_bytes(1,'big'))

def lin_write_id(lin_id):
     
    lin_id = lin_id | lin_parity(lin_id)  # Add parity
    
    uart0.sendbreak()
    uart0.write(b'\x55')
    uart0.write(lin_id.to_bytes(1,'big'))
   # uart0.txdone()
    
def lin_read(data,len):
    time.sleep(1)
    lin_id = lin_id | lin_parity(lin_id)
    
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

print("Raspberry Pi Pico LIN-bus Master read demo. skpang.co.uk 2023")

    
while 1:
   
    led.value(1)

    start_time = time.ticks_ms()

    lin_write_id(SLAVE_ADDRESS)
    
    rxData = bytes()
    while time.ticks_diff(time.ticks_ms(), start_time) < 100:
        while uart0.any() > 0:
            rxData += uart0.read(1)
    

    l = len(rxData)
    
    for x in range(l-2):
        print(' ', end='')
        print(hex(rxData[x+2]), end='')    #ignore the first 2 bytes, it is echo of break and 0x55
    
    print(' ')
    
    led.value(0)
    time.sleep(0.1)




