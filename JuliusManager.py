import os
import signal
import socket
import subprocess
import time
from typing import Dict, List


class JuliusManager:
    def __init__(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.process = None
        try:
            self.sock.connect((host, port))
        except ConnectionRefusedError as _:
            self.run_terminal()
            if self.process is None:
                raise ConnectionRefusedError("Could not connect to julius.")
            try:
                self.sock.connect((host, port))
            except ConnectionRefusedError as _:
                raise ConnectionRefusedError("Could not connect to julius.")
        else:
            self.sock.setblocking(False)
        self.data = ""
        self.__wake_words = {"水ください": 1}

    def terminate(self) -> None:
        if self.process is not None:
            if os.name == "nt":
                os.kill(self.process.pid, signal.CTRL_C_EVENT)
            else:
                os.kill(self.process.pid, signal.SIGKILL)
        time.sleep(1)

    def __del__(self) -> None:
        self.terminate()

    def run_terminal(self) -> None:
        if os.name == "nt":
            # for windows
            path = "julius-start.cmd"
            if os.path.exists(path):
                self.process = subprocess.Popen(
                    f'start "JULIUS CONSOLE" cmd.exe /K "{path}"', shell=True
                )
                time.sleep(2)
            else:
                self.terminate()
                raise FileNotFoundError(f"{path} file not found.")
        else:
            # for linux or mac
            path = "julius-start.sh"
            if os.path.exists(path):
                self.process = subprocess.Popen(f'xterm -hold -e "{path}"', shell=True)
            else:
                self.terminate()
                raise FileNotFoundError(f"{path} file not found.")

    @property
    def wake_words(self) -> dict:
        return self.__wake_words

    @wake_words.setter
    def wake_words(self, wake_words: Dict[str, int]) -> None:
        if type(wake_words) is not dict:
            raise TypeError("`wake_words` should be `dict` type.")
        else:
            self.__wake_words = wake_words

    def update(self) -> List[int]:
        spoken_id_list = []
        is_data_remaining = True
        while is_data_remaining:
            try:
                self.data += str(self.sock.recv(1024).decode("utf-8"))
            except BlockingIOError as _:
                # Juliusから何も来ていなかったときに起こる例外
                is_data_remaining = False

        if "</RECOGOUT>\n." in self.data:
            for line in self.data.split("\n"):
                index = line.find('WORD="')
                if index != -1:
                    spoken = line[index + 6 : line.find('"', index + 6)]
                    spoken_id = self.__wake_words.get(spoken)
                    if spoken_id:
                        spoken_id_list.append(spoken_id)
            self.data = ""

        return spoken_id_list
