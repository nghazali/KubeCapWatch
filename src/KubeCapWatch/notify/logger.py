import datetime
from pathlib import Path
from os import path

class log_notifier:
    def __init__(self, agent_name, logfile):
        self.agent_name = agent_name
        self.logfile = file = (f"{Path().absolute()}/../../log/{logfile}")

        # Posting to the Console
    def notify(self, text):
        if text == '':
            return

        if ~path.isfile(self.logfile):
            self.__generate_log_file()

        lines = text.splitlines(True)
        with open(self.logfile, 'a') as f:
            f.write(f"{datetime.datetime.now()} {self.agent_name}: ")
            f.writelines(lines)

    def __generate_log_file(self):
        if ~path.isfile(self.logfile):
            with open(self.logfile, 'w') as f:
                f.writelines([f'KubeCapWatch log - generated at {datetime.datetime.now()}'])


