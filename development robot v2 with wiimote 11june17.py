import RPi.GPIO as gpio
import time
import cwiid, time
gpio.setwarnings(False)
gpio.cleanup()
#INITIAL SETUP
gpio.setmode(gpio.BCM)
#enable_pin=17
#gpio.setup(enable_pin, gpio.OUT)
#gpio.output(enable_pin, gpio.LOW)

left_forward=22
left_reverse=23
right_forward=25
right_reverse=24

gpio.setup(left_forward, gpio.OUT)
gpio.setup(left_reverse, gpio.OUT)
gpio.setup(right_forward, gpio.OUT)
gpio.setup(right_reverse, gpio.OUT)

def reset_all():
 #set all GPIOs to low
        gpio.output(left_forward, gpio.LOW)
        gpio.output(left_reverse,gpio.LOW)
        gpio.output(right_forward, gpio.LOW)
        gpio.output(right_reverse,gpio.LOW)

def go(direction, duration):
        reset_all()
        #pwm=gpio.PWM(enable_pin, 80)
        #pwm.start(speed)
        #pwm.ChangeDutyCycle(speed)
        if direction=="forward":
                gpio.output(right_forward, gpio.HIGH)
                gpio.output(left_forward, gpio.HIGH)
        elif direction=="reverse":
                gpio.output(right_reverse,gpio.HIGH)
                gpio.output(left_reverse,gpio.HIGH)
        elif direction=="left":
                gpio.output(left_reverse, gpio.HIGH)
                gpio.output(right_forward, gpio.HIGH)
        elif direction=="right":
                gpio.output(right_reverse, gpio.HIGH)
                gpio.output(left_forward, gpio.HIGH)
        elif direction=="stop":
                gpio.output(right_reverse, gpio.LOW)
                gpio.output(left_forward, gpio.LOW)
                gpio.output(right_forward, gpio.LOW)
                gpio.output(left_reverse, gpio.LOW) 
        time.sleep(duration)
        #pwm.stop()
        reset_all()

# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following lines of code demonstrate many of the features realted to wiimotes, such as capturing button presses and rumbling the controller.
# I have managed to map the home button to the accelerometer - simply hold it and values will appear!

# Coded by The Raspberry Pi Guy. Work based on some of Matt Hawkins's!

button_delay = 0.0

print ('Please press buttons 1 + 2 on your Wiimote now ...')
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
  wii=cwiid.Wiimote()
except RuntimeError:
  print ("Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!")
  quit()

print ('Wiimote connection established!\n')
print ('Go ahead and press some buttons\n')
print ('Press PLUS and MINUS together to disconnect and quit.\n')

time.sleep(3)

wii.rpt_mode = cwiid.RPT_BTN

while True:

  buttons = wii.state['buttons']

  # Detects whether + and - are held down and if they are it quits the program
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print ('\nClosing connection ...')
    # NOTE: This is how you RUMBLE the Wiimote
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)


  # The following code detects whether any of the Wiimotes buttons have been pressed and then prints a statement to the screen!
  if (buttons & cwiid.BTN_LEFT):
    print ('Left pressed')
    go("left",0.5)
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    print ('Right pressed')
    go("right",1)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    print ('Up pressed')
    go("forward", 2)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    print ('Down pressed')
    go("reverse",1)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_1):
    print ('Button 1 pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_2):
    print ('Button 2 pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    print ('Button A pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_B):
    print ('Button B pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_HOME):
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    check = 0
    while check == 0:
      print(wii.state['acc'])
      time.sleep(0.01)
      check = (buttons & cwiid.BTN_HOME)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    print ('Minus Button pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    print ('Plus Button pressed')
    time.sleep(button_delay)

                        
#def take_photo():
        #pic=picam.takePhotoWithDetails(640,480,75)
        #filename="image" +time.strftime("%Y%m%d-%H%M%S")+".jpg"
        #pic.save(filename)

#take_photo()

gpio.cleanup()

