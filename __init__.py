from flask import Flask, request, render_template, jsonify
import RPi.GPIO as GPIO
import time
from flask_mail import Mail, Message
import ConfigParser
import os


shutdown = False

parser = ConfigParser.ConfigParser()
parser.read(os.path.expanduser('/home/pi/Desktop/.config.txt'))


app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS= True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'edwinyjlim@gmail.com',
    MAIL_PASSWORD = parser.get('important', 'email_pw')
))


mail = Mail(app)
the_punchline = parser.get('important', 'punchline')



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
def hello_world():
    if shutdown:
        return "shutdown variable enabled"
    return render_template('index.html')

@app.route('/knockknock')
def knockknock():
    if shutdown:
        return "shutdown variable enabled"
    return render_template('knockknock.html')

@app.route('/punchline', methods=['POST'])
def punchline():
    if shutdown:
        return "shutdown variable enabled"
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
    if shutdown:
        return "shutdown variable enabled"
    punchline = request.form.get('punchline')
    door_status = 'closed'
    msg = Message("RPi buzzed open the door",
                  sender="edwinyjlim@gmail.com",
                  recipients=["edwinyjlim@gmail.com"])
    msg.body = "delivered by Flask mail"
                  
    if punchline == the_punchline:
        activate_GPIO(7,7)
        door_status = 'open'
        mail.send(msg)
                  
    return jsonify(door_status=door_status)


@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown_server():
    global shutdown
    shutdown = True
    return 'Server shutdown variable set to True.'

if __name__ == "__main__":
    app.run()
        
