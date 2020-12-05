import os
import subprocess
run_str="bokeh serve --show new.py"

subprocess.call("python colorpicker.py")
subprocess.call(run_str)