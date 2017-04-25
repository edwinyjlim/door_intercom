from flask import Flask, request, render_template
import RPi.GPIO as GPIO
import time
from datetime import date

app = Flask(__name__)



@app.context_processor
def inject_template_globals():
    return {
        'ts': time.clock(),
    }


def set_GPIO (pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

def reset_GPIO():
    GPIO.cleanup()
    
def blink_GPIO (pin, blink_count):
    set_GPIO(pin)
    for i in range(0, blink_count):
        GPIO.output(pin, 1)
        time.sleep(1)
        GPIO.output(pin, 0)
        time.sleep(1)
    reset_GPIO()
    return

def activate_GPIO (pin, duration):
    set_GPIO(pin)
    GPIO.output(pin, 1)
    time.sleep(duration)
    GPIO.output(pin, 0)
    reset_GPIO()
    return


@app.route('/')
def hell_world():
    return render_template('index.html')

@app.route('/knockknock')
def knockknock():
    return render_template('knockknock.html')
    

@app.route('/flashlight')
def flashlight():
    blink_GPIO(7,3)
    return 'Flashing GPIO pin 3 times'

@app.route('/activate')
def activate():
    activate_GPIO(7,5)
    return 'Activating GPIO pin for 5 seconds'


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    print 'callback'
    return 'callback'


@app.route('/error', methods=['GET', 'POST'])
def error():
    print 'Something went wrong...'
    return 'Something went wrong...'


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
        
