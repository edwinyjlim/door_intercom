from flask import Flask, request, render_template, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

the_punchline = 'green'

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

@app.route('/punchline', methods=['POST'])
def punchline():
    
    punchline = request.form.get('punchline')
    print 'user submitted passphrase: '+punchline
    
    door_status = 'closed'
    message = 'Incorrect passphrase.'
    
    if punchline == the_punchline:
        door_status = 'open'
        message = 'Welcome.'
        
    return jsonify(door_status=door_status,
                   message=message);

@app.route('/buzzer', methods=['POST'])
def buzzer():
    punchline = request.form.get('punchline')
    door_status = 'closed'
    if punchline == the_punchline:
        activate_GPIO(7,7)
        door_status = 'open'
    return jsonify(door_status=door_status)

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
        
