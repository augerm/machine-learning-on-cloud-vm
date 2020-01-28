import subprocess
import re
from shutil import copyfile
import json
class System:
    @staticmethod
    def run_command(command):
        # https://stackoverflow.com/a/16710842g
        command_arr = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', command)
        result = subprocess.check_output(command_arr).decode('utf-8')
        return result
    @staticmethod
    def copy_file_to(current_location, target_location):
        copyfile(current_location, target_location)
    @staticmethod
    def write_json_to_file(data, target_location):
        with open(target_location, 'w') as f:
            json.dump(data, f)