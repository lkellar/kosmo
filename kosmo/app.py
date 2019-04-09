from flask import Flask, request, render_template, jsonify
from .face import Face
from os import path
import json

app = Flask(__name__, static_folder='../static', static_url_path='/static',
            template_folder='../templates')

f = Face()
currentDir = path.dirname(path.realpath(__file__))
configPath = path.join(currentDir, '../', 'config.json')
config = []


@app.before_first_request
def initFace():
    global config
    # Checks to see if a config.json exists, and if so, creates a bot from it
    if path.exists(configPath):
        print('Config Found! Creating Face from config')

        with open(configPath, 'r') as file:
            config = json.load(file)

        if 'parts' in config:
            for i in config['parts']:
                f.addPart(i)
    else:
        print('No config found, an empty face has been created')


# Main Dashboard
@app.route('/')
def index():
    return render_template('index.html', face=f, PartSorter=PartSorter)


@app.route('/add', methods=['POST'])
def addParts():
    global f
    # A form can be passed as a multipart or json
    parts = fetchBody(request)

    # Bulk requests are also supported. If a user submits a json array with command objects inside,
    # it'll handle them all
    if type(parts) == list:
        for i in parts:
            f.addPart(dict(i))
    else:
        f.addPart(dict(parts))

    return '200 OK'


@app.route('/control', methods=['POST'])
def controlParts():
    # A form can be passed as a multipart or json
    commands = fetchBody(request)

    # Bulk requests are also supported. If a user submits a json array with command objects inside,
    # it'll handle them all
    if type(commands) == list:
        for i in commands:
            processCommand(i)
    else:
        processCommand(commands)

    # After a control request, the current angle status for all servos is returned
    # This is useful for the dashboard, so that all angles are updated, regardless of where they were changed
    return jsonify({key: value.getAngles() for key, value in f.fetchParts().items()})


@app.route('/save')
def saveConfig():
    global config
    # Saves the current setup into a config file outside of the src folder
    config['parts'] = [i.getConfig() for i in f.fetchParts().values()]
    with open(configPath, 'w') as file:
        json.dump(config, file)

    return jsonify(config)


@app.route('/speak', methods=['POST'])
def speakAudio():
    # A form can be passed as a mutlipart or json
    commands = fetchBody(request)
    if not f.mouth:
        raise InvalidUsage('No Mouth available to control')
    if 'text' not in f.mouth:
        raise InvalidUsage('Text argument not found')
    if 'angry' not in f.mouth:
        commands['angry'] = False
    f.mouth.speak(commands['text'], commands['angry'])

    return '200 OK'


def fetchBody(r: request):
    # A form can be passed as a multipart or json
    if r.is_json:
        return r.get_json()
    else:
        return r.form.to_dict(flat=True)


def processCommand(command: dict):
    # This allows the special speak command to jump the line!
    if command['cmd'] == 'speak':
        f.mouth.speak(command['text'], True if 'angry' in command else False)
        return

    # Takes a command object and processes it
    part = f.fetchParts()[command['part']]
    if command['axis'].lower() == 'x':
        servo = part.x
    elif command['axis'].lower() == 'y':
        servo = part.y
    else:
        # If the axis arg isn't x or y, something is wrong
        raise InvalidUsage("Axis must be 'X' or 'Y'")

    # if the cmd is a mid, max, or min, no angle is needed, and we can just call the corresponding function
    if command['cmd'] in ['mid', 'max', 'min']:
        getattr(servo, command['cmd'])()
    elif command['cmd'] == 'set':
        # if the cmd is set, we set the servo to the angle provided
        servo.setPosition(float(command['angle']))
    else:
        # and of course, if an invalid cmd is passed, throw an error
        raise InvalidUsage("cmd must be 'mid', 'max', 'min' or 'set'!")


class PartSorter:
    # This iterator puts the parts in order on the dashboard, so rightEye isn't on the left of leftEye for example.
    def __init__(self, parts):
        self.parts = parts
        # This is the proper alignment for the parts
        self.alignment = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'mouth']
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.alignment):
            raise StopIteration
        else:
            name = self.alignment[self.current]
            part = self.parts.get(name)
            self.current += 1
            if not part:
                # if a part isn't found, just continue on to the next name in alignment
                return self.__next__()
            else:
                return name, part


class InvalidUsage(Exception):
    status_code = 400
    # Basic API Exception thrown at the user

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
    # Basic error handler for the InvalidUsage
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run()
