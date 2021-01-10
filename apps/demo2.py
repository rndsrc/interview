import os
import subprocess
run_str="bokeh serve --show new.py"
subprocess.call("python colorpicker.py",shell=True)

subprocess.call("bokeh serve --show new.py",shell=True)
