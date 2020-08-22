import datetime
import os
import signal
import socket
import subprocess
import time
from pathlib import Path

from termcolor import cprint


class JuliusManager:
    def __init__(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.process = None
        try:
            self.sock.connect((host, port))
        except ConnectionRefusedError as _:
            # self.end()
            # cprint("Could not connected to julius.", color="red")
            # cprint("Run 'sh julius-start.sh'.", color="red")
            # raise Exception("Could not connected to julius.")
            self.run_terminal()
            if self.process is None:
                raise Exception("Could not connected to julius.")
            try:
                self.sock.connect((host, port))
            except ConnectionRefusedError as _:
                raise Exception("Could not connected to julius.")
        else:
            cprint("Connected to julius.", color="green")
            self.sock.setblocking(False)
        self.data = ""
        self.start_word = "録画開始"
        self.stop_word = "終わりましたよ"
        self.flag_should_start_recording = False
        self.flag_should_stop_recording = False

    def terminate(self):
        if self.process is not None:
            if os.name == "nt":
                os.kill(self.process.pid, signal.CTRL_C_EVENT)
            else:
                os.kill(self.process.pid, signal.SIGKILL)
        time.sleep(1)

    def __del__(self):
        self.terminate()

    def run_terminal(self) -> None:
        if os.name == "nt":
            # for windows
            path = "julius-start.cmd"
            if os.path.exists(path):
                self.process = subprocess.Popen("start \"JULIUS CONSOLE\" cmd.exe /K \"{}\"".format(path), shell=True)
                time.sleep(2)
            else:
                self.terminate()
                raise Exception("{} file not found.".format(path))
        else:
            # for linux or mac
            # 未検証
            path = "julius-start.sh"
            if not os.path.exists(path):
                self.process = subprocess.Popen("xterm -hold -e \"{}\"".format(path), shell=True)
            else:
                self.terminate()
                raise Exception("{} file not found.".format(path))

    def set_parameter(self, start_word: str, stop_word: str) -> None:
        self.start_word = start_word
        self.stop_word = stop_word

    def update(self) -> None:
        if "</RECOGOUT>\n." in self.data:
            spoken = ""
            for line in self.data.split("\n"):
                index = line.find('WORD="')
                if index != -1:
                    line = line[index + 6: line.find('"', index + 6)]
                    spoken += str(line)
            self.data = ""

            # print("Detected: " + spoken)
            if self.start_word in spoken:
                self.flag_should_start_recording = True
            elif self.stop_word in spoken:
                self.flag_should_stop_recording = True

        else:
            try:
                self.data += str(self.sock.recv(1024).decode("utf-8"))
            except BlockingIOError as e:
                # Juliusから何も来ていなかったときに起こる例外
                pass

    def should_start_recording(self) -> bool:
        if self.flag_should_start_recording:
            self.flag_should_start_recording = False
            return True
        else:
            return False

    def should_stop_recording(self) -> bool:
        if self.flag_should_stop_recording:
            self.flag_should_stop_recording = False
            return True
        else:
            return False
