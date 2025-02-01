from flask import Flask, request
app = Flask(__name__)
import windows_interaction

@app.route('/sessions')
def update_sound_mixer():
    """Update the list of audio sessions"""
    response = windows_interaction.get_audio_sessions()
    new_sessions = list(response.keys())
    return new_sessions

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

if  __name__ == '__main__':
    app.run(debug=True)
