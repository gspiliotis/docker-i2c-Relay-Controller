# todo: Implement Signals to notify the app whenever the relay status changes
# todo: use web sockets to update the status display when the relay status changes
from __future__ import print_function

import json
import os
from flask import Flask, request #Needs python3-flask
from flask import make_response
from flask import render_template
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap

from relays import Relays
from relayType import RelayType


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


bootstrap = Bootstrap(app)

def get_message(msg):
    return "{'msg': '"+msg+"'}"

@app.route('/')
def index():
    print("Loading app Main page")
    # return success_resp
    return render_template('index.html')


@app.route('/all/status')
def api_relay_all_status():
    status = Relays.get_relays_raw()
    return make_response(json.dumps(status), 200)

@app.route('/all/on')
def api_relay_all_on():
    Relays.on()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("ALL Turned ON OK"), 200)


@app.route('/all/off')
def api_all_relay_off():
    Relays.off()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("ALL Turned ON OK"), 200)

@app.route('/all/toggle')
def api_all_relay_toggle():
    Relays.toggle()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("ALL Toggled OK"), 200)

#Create relay
@app.route('/', methods = ['PUT'])
def api_add_relay():
    relayStr = request.form['data']
    print(relayStr)

    relay = Relays.add(relayStr)
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(relay.to_JSON(),  200)

#Delete relay
@app.route('/<int:relay_id>', methods = ['DELETE'])
def api_delete_relay(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    Relays.delete(relay_id)
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response("", 200)

#Relay Name
@app.route('/<int:relay_id>/name', methods = ['GET', 'POST'])
def api_get_name(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    relay = Relays.get_relay(relay_id)
    if request.method == 'POST':
        print(request.form['data'])
        relay.set_name(json.loads(request.form['data']))
    return make_response(json.dumps(relay.get_name()), 200)


#Relay Description
@app.route('/<int:relay_id>/description', methods = ['GET', 'POST'])
def api_get_description(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    relay = Relays.get_relay(relay_id)
    if request.method == 'POST':
        print(request.form['data'])
        relay.set_description(json.loads(request.form['data']))
    return make_response(json.dumps(relay.get_description()), 200)

#Relay notes
@app.route('/<int:relay_id>/notes', methods = ['GET', 'POST'])
def api_get_notes(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    relay = Relays.get_relay(relay_id)
    if request.method == 'POST':
        print(request.form['data'])
        relay.set_notes(json.loads(request.form['data']))
    return make_response(json.dumps(relay.get_notes()), 200)

#Relay Inverted
@app.route('/<int:relay_id>/inverted', methods = ['GET', 'POST'])
def api_get_inverted(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    relay = Relays.get_relay(relay_id)
    if request.method == 'POST':
        print(request.form['data'])
        relay.set_inverted(json.loads(request.form['data']))
        socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(json.dumps(relay.get_inverted()), 200)

#Relay Status
@app.route('/<int:relay_id>/status')
def api_get_status(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    status = Relays.get_relay(relay_id).get_status()
    if status:
        return make_response("1", 200)
    else:
        return make_response("0", 200)

#Relay Toggle
@app.route('/<int:relay_id>/toggle')
def api_toggle_relay(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    Relays.get_relay(relay_id).toggle()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("Toggled OK"), 200)



# Relay ON
@app.route('/<int:relay_id>/on')
def api_relay_on(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    Relays.get_relay_byId(relay_id).on()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("Turned ON OK"), 200)


# Relay OFF
@app.route('/<int:relay_id>/off')
def api_relay_off(relay_id):
    if not Relays.is_valid_relayId(relay_id):
        return make_response(get_message("Invalid ID: "+str(relay_id)), 404)
    Relays.get_relay_byId(relay_id).off()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("Turned OFF OK"), 200)

# Scan
@app.route('/scan/<int:bus>')
def api_scan(bus):
    scanOutput = os.popen("i2cdetect -y "+str(bus)).read()
    return make_response(scanOutput, 200)

# Types
@app.route('/types')
def api_types():
    return make_response(json.dumps(RelayType.get_types()), 200)


@app.errorhandler(404)
def page_not_found(e):
    print("ERROR: 404")
    return render_template('404.html', the_error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    print("ERROR: 500")
    return render_template('500.html', the_error=e), 500


if __name__ == "__main__":
    PORT = os.getenv('PORT', 1080)
    DEBUG = os.getenv('DEBUG', False)
    if DEBUG:
        socketio.run(app, host='0.0.0.0', port=PORT, debug=True)
    else:
        socketio.run(app, host='0.0.0.0', port=PORT)
