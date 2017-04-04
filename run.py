import os
from flask import Flask, request, render_template
import shlex
from subprocess import Popen, PIPE

root_dir = '/home/pi/hal-run/hal-run-app'
music_dir = root_dir + '/static/music'
effects_dir = root_dir + '/static/effects'



app = Flask(__name__)

def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err

@app.route('/')
@app.route('/home')
def index():
    music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
    music_files_number = len(music_files)
    return render_template("index.html",
                        title = 'Home',
                        music_files_number = music_files_number,
                        music_files = music_files)

@app.route('/ef/<effect_name>')
def start_ffect(effect_name=None):
    cmd = "pkill " + app.debug 
    get_exitcode_stdout_stderr(cmd); # remove previous effect
    app_name = effect_name + "_demo"
    curr_effect = app_name #comments
    cmd = "./static/effects/" + app_name
    get_exitcode_stdout_stderr(cmd);

    

@app.route('/pl/<filename>')
def song(filename):
    return render_template('play.html',
                        title = filename,
                        music_file = filename)

def sounds_cleaner():
    #while (true) monitoring sounds dir
    pass

if __name__ == '__main__':
    global curr_effect = None
    app.run(host = '0.0.0.0', debug = True)
