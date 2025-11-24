import sys
import time
import platform
import subprocess
from pynput import mouse
import pyttsx3


class WorkstationLocker:
    def lock(self):
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run("rundll32.exe user32.dll,LockWorkStation", check=True)
            elif system == "Darwin":
                subprocess.run(["pmset", "displaysleepnow"], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-screensaver", "lock"], check=True)
            else:
                return False
            return True
        except:
            return False


class Speaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
        except:
            self.engine = None

    def say(self, text):
        if not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass


class MouseGuard:
    def __init__(self):
        self.triggered = False
        self.locker = WorkstationLocker()
        self.speaker = Speaker()

    def on_move(self, x, y):
        if not self.triggered:
            self.triggered = True
            print("Movement detected… Initiating chaos sequence.")
            locked = self.locker.lock()

            if locked:
                time.sleep(1)
                self.speaker.say(
                    "You have been locked out for your crimes against personal boundaries!"
                )
                time.sleep(1)
                self.speaker.say(
                    "Next time, try asking permission instead of acting like a ninja raccoon."
                )
                time.sleep(1)
                print("Mission complete. Shutting down script.")
                sys.exit(0)
            else:
                print("Locking attempt failed. The universe remains chaotic.")
                self.triggered = False

    def start(self):
        try:
            with mouse.Listener(on_move=self.on_move) as listener:
                print("Guardian active. Move the mouse if you dare.")
                listener.join()
        except KeyboardInterrupt:
            print("Shutdown requested. Retreating gracefully.")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected meltdown: {e}")
            sys.exit(1)


if __name__ == "__main__":
    print("Booting guardian in 5 seconds...")
    time.sleep(5)
    MouseGuard().start()
