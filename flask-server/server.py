from flask import Flask, request
app = Flask(__name__)
import windows_interaction

@app.route('/members')
def members():
    return {"members": ["Member1","Member2"]}

@app.route('/sessions')
def update_sound_mixer():
    all_sessions = []
    new_sessions = windows_interaction.update_sessions()
    """Update the list of audio sessions and refresh the GUI."""
    current_processes = set(all_sessions)
    new_processes = set(new_sessions)
    print(current_processes)
    print(new_processes)
    return new_sessions
    # Add new processes
    for process_name in new_processes - current_processes:
        add_session(process_name)

    # Remove closed processes
    for process_name in current_processes - new_processes:
        all_sessions.remove(process_name)
        remove_session(process_name)
    all_sessions = new_sessions

@app.route('/volume', methods=['GET'])
def set_volume():
    process_name = request.args.get('process_name')
    volume_val = float(request.args.get('volume_val'))
    response = windows_interaction.set_volume(process_name, volume_val)
    return response

@app.route('/mute', methods=['GET'])
def toggle_mute():
    process_name = request.args.get('process_name')
    response = windows_interaction.toggle_mute(process_name)
    return response

#def add_session(process_name):
#    socketio.emit('add_controller', {'process_name': process_name})
#
#def remove_session(process_name):
#    socketio.emit('remove_controller', {'process_name': process_name})

if  __name__ == '__main__':
    app.run(debug=True)
