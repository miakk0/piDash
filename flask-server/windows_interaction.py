from pycaw.pycaw import AudioUtilities
import keyboard
import comtypes
import os
class AudioController:
    """Creates an object based on the process name of the session (e.g. msedge.exe), allowing the control of the audio (volume & mute state)"""
    def __init__(self, process_name, audio_interface):
        self.process_name = process_name
        self.audio_interface = audio_interface

    def mute(self):
        self.audio_interface.SetMute(1, None)

    def unmute(self):
        self.audio_interface.SetMute(0, None)

    def is_muted(self):
        return self.audio_interface.GetMute()

    def get_volume(self):
        return self.audio_interface.GetMasterVolume()

    def set_volume(self, volume):
        self.audio_interface.SetMasterVolume(volume, None)

def get_audio_sessions():
    """Retrieve all active audio sessions and their controllers."""
    comtypes.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    audio_controllers = {}
    for session in sessions:
        if session.Process:
            interface = session.SimpleAudioVolume
            audio_controllers[session.Process.name()] = AudioController(
                session.Process.name(), interface
            )
    return audio_controllers

def set_volume(process_name: str, value: str):
    """Set volume for a specific audio session."""
    if 0 < value < 1:
        audio_sessions = get_audio_sessions()
        for _, (name, controller) in enumerate(audio_sessions.items()):
            if name == process_name:
                controller.set_volume(float(value))
                return f"Set volume for {controller.process_name} to {value}"
        else:
            controller = None
            return "Couldn't find controller"
    else:
        return "Invalid value for volume (must be between 0 and 1)" #To be deleted later since sliders already limits the range

def toggle_mute(process_name: str):
        """Toggle mute/unmute for a specific audio session."""
        audio_sessions = get_audio_sessions()
        for _, (name, controller) in enumerate(audio_sessions.items()):
            if name == process_name:
                if controller.is_muted():
                    controller.unmute()
                    text = f"{process_name} unmuted"
                else:
                    controller.mute()
                    text = f"{process_name} muted"
                return text
        
def play_pause():
    try:
        keyboard.send('play/pause')  # Simulate Play/Pause key
        #return "Play/Pause pressed"
    except Exception:
        print("Error")


def open_app(app_name: str):
    print(app_name)
    try:
        os.system(f'start "" "{app_name}"')
        return f"{app_name} opened"
    except FileNotFoundError:
        return f"{app_name} could not be found"
    
