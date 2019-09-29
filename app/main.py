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

@app.route('/<int:relay_index>/notes', methods = ['GET', 'POST'])
def api_get_notes(relay_index):
    if not Relays.is_valid_relayIndex(relay_index):
        return make_response(get_message("Relay index out of range: "+str(relay_index)), 404)
    relay = Relays.get_relay_byIndex(relay_index)
    if request.method == 'POST':
        print(request.form['data'])
        relay.set_notes(str(request.form['data']))
    return make_response(relay.get_notes(), 200)

@app.route('/<int:relay_index>/name', methods = ['GET', 'POST'])
def api_get_name(relay_index):
    if not Relays.is_valid_relayIndex(relay_index):
        return make_response(get_message("Relay index out of range: "+str(relay_index)), 404)
    relay = Relays.get_relay_byIndex(relay_index)
    if request.method == 'POST':
        print(request.form['data'])
        relay.set_name(str(request.form['data']))
    return make_response(relay.get_name(), 200)


@app.route('/<int:relay_index>/status')
def api_get_status(relay_index):
    if not Relays.is_valid_relayIndex(relay_index):
        return make_response(get_message("Relay index out of range: "+str(relay_index)), 404)
    status = Relays.get_relay_byIndex(relay_index).get_status()
    if status:
        return make_response("1", 200)
    else:
        return make_response("0", 200)


@app.route('/<int:relay_index>/toggle')
def api_toggle_relay(relay_index):
    if not Relays.is_valid_relayIndex(relay_index):
        return make_response(get_message("Relay index out of range: "+str(relay_index)), 404)
    Relays.get_relay_byIndex(relay_index).toggle()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("Toggled OK"), 200)




@app.route('/<int:relay_index>/on')
def api_relay_on(relay_index):
    if not Relays.is_valid_relayIndex(relay_index):
        return make_response(get_message("Relay index out of range: "+str(relay_index)), 404)
    Relays.get_relay_byIndex(relay_index).on()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("Turned ON OK"), 200)


@app.route('/<int:relay_index>/off')
def api_relay_off(relay_index):
    if not Relays.is_valid_relayIndex(relay_index):
        return make_response(get_message("Relay index out of range: "+str(relay_index)), 404)
    Relays.get_relay_byIndex(relay_index).off()
    socketio.emit('updated_relays_status', Relays.get_relays_raw())
    return make_response(get_message("Turned OFF OK"), 200)



@app.errorhandler(404)
def page_not_found(e):
    print("ERROR: 404")
    return render_template('404.html', the_error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    print("ERROR: 500")
    return render_template('500.html', the_error=e), 500


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80)
