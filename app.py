from flask import Flask
from twilio.rest import TwilioRestClient
import RPi.GPIO as GPIO
import time
from datetime import date

app = Flask(__name__)


# twilio account
tw_account_sid = "AC1d50cb742f20a3ba02d3469389b261d1"
tw_auth_token = "a4e877d10da778251189c9d07c250f34"
tw_phone_num = "+13108538839"
tw_client = TwilioRestClient(tw_account_sid, tw_auth_token)

my_phone_num = "+13108923481"


#RPi GPIO configs and functions
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
def LED_blink(pin):
    GPIO.output(pin, 1)
    time.sleep(1)
    GPIO.output(pin, 0)
    time.sleep(1)
    return

def flash_LED (pin, blink_count):
    for i in range(0, blink_count):
        LED_blink(pin)
    

@app.route('/')
def hell_world():
    return 'HELLOOOOOOO WORLD ' + str(time.ctime())

@app.route('/textme')
def text_me():
    flash_LED(7, 3)
    GPIO.cleanup()
    tw_client.messages.create(
        to=my_phone_num,
        from_=tw_phone_num,
        body="this is my RPi test SMS sent on " + str(time.ctime())
    )
    return 'Twilio sent you a test text -- check your phone'

@app.route('/texttwilio')
def text_twilio():
    flash_LED(7, 3)
    GPIO.cleanup()
    tw_client.messages.create(
        to=tw_phone_num,
        from_=tw_phone_num,
        body="Hi Twilio, this is my test SMS sent on " + str(time.ctime())
    )
    return 'You sent Twilio a test text'


if __name__ == "__main__":
    app.run(debug=True)
        
