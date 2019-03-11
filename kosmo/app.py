from flask import Flask, request, render_template, jsonify
from kosmo.face import Face
from os import path
import json

app = Flask(__name__, static_folder='../static', static_url_path='/static',
            template_folder='../templates')

f = Face()


@app.before_first_request
def initFace():
    # Checks to see if a config.json exists, and if so, creates a bot from it
    currentDir = path.dirname(path.realpath(__file__))
    configPath = path.join(currentDir, '../', 'config.json')
    if path.exists(configPath):
        print('Config Found! Creating Face from config')

        with open(configPath, 'r') as file:
            config = json.load(file)

        for i in config:
            f.addPart(i)

    else:
        print('No config found, an empty face has been created')


@app.route('/')
def index():
    return render_template('index.html', face=f)


@app.route('/add', methods=['POST'])
def addParts():
    global f
    # A config is passed as a json body, so we're just going to pass that right along
    config = request.get_json()

    if type(config) == list:
        for i in config:
            f.addPart(i)
    else:
        f.addPart(config)

    return '200 OK'


@app.route('/control', methods=['POST'])
def controlParts():
    commands = request.get_json()

    if type(commands) == list:
        for i in commands:
            processCommand(i)
    else:
        processCommand(commands)


    return '200 OK'


def processCommand(command: dict):
    part = f.fetchParts()[command['part']]
    if command['axis'].lower() == 'x':
        servo = part.x
    elif command['axis'].lower() == 'y':
        servo = part.y
    else:
        raise InvalidUsage("Axis must be 'X' or 'Y'")

    if command['cmd'] in ['mid', 'max', 'min']:
        getattr(servo, command['cmd'])()
    elif command['cmd'] == 'set':
        servo.setPosition(command['angle'])
    else:
        raise InvalidUsage("cmd must be 'mid', 'max', 'min' or 'set'!")


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run()
