from flask import Flask, request, render_template
from .face import Face
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

if __name__ == '__main__':
    app.run()
