from pycaw.pycaw import AudioUtilities
import keyboard
import comtypes
from comtypes import COMError
class AudioController:
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

audio_sessions = {}
audio_sessions_process_names = []

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

def update_sessions():
    """Update the list of audio sessions and refresh the GUI."""
    
    new_sessions = get_audio_sessions()
    
    current_processes = set(audio_sessions.keys())
    new_processes = set(new_sessions.keys())
    
    # Add new processes
    for process_name in new_processes - current_processes:
        controller = new_sessions[process_name]
        audio_sessions[process_name] = controller
        #self.add_session_to_gui(process_name, controller)

    # Remove closed processes
    for process_name in current_processes - new_processes:
        audio_sessions.pop(process_name, None)
        #self.remove_session_from_gui(process_name)
    return list(audio_sessions.keys())


def set_volume(process_name, value):
    """Set volume for a specific audio session."""
    audio_sessions = get_audio_sessions()
    for _, (name, controller) in enumerate(audio_sessions.items()):
        if name == process_name:
            controller.set_volume(float(value))
            return f"Set volume for {controller.process_name} to {value}"
    else:
        controller = None
        return "Couldn't find controller"
    #controller = next((audio_session for audio_session in audio_sessions if audio_session.process_name == process_name), None)

def get_volume(process_name):
    """Get volume for a specific audio session."""
    print(audio_sessions)
    for _, (name, controller) in enumerate(audio_sessions.items()):
        print(name)
        if name == process_name:
            return str(controller.get_volume())
            #print(f"Set volume for {controller.process_name} to {value}")
            #break
    else:
        controller = None
        print("Couldn't find controller")

def toggle_mute(process_name):
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
        
def is_muted(process_name):
    for _, (name, controller) in enumerate(audio_sessions.items()):
        if name == process_name:
            if controller.is_muted():
                button_text = "Unmute"
            else:
                button_text = "Mute"
            return button_text
        
def play_pause():
    try:
        keyboard.send('play/pause')  # Simulate Play/Pause key
        #return "Play/Pause pressed"
    except Exception:
        print("Error")

