import os, signal
from flask import Flask, jsonify, request, render_template
import shlex
from subprocess import Popen, PIPE
import psutil
from time import sleep


root_dir = '/home/pi/hal-run/hal-run-app'
music_dir = root_dir + '/static/music'
effects_dir = root_dir + '/static/effects'



app = Flask(__name__)
app.config['curr_effect'] = "None"
app.config['start_cycle'] = False

def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)
    p = psutil.Popen(args, stdout=PIPE)
    print('Proc STARTED - ' + p.name())

def clearEffects():
    print('Trying to delete -- ' + app.config["curr_effect"])
    procName = app.config["curr_effect"]
    for proc in psutil.process_iter():
        if proc.name() == procName:
            print(proc)
            proc.kill()
            os.kill(proc.pid, signal.SIGKILL)


def clearAllEffects():
    allEffects = ['everloop_demo', 'arc_demo', 'direction_of_arrival_demo', 'mic_energy']
    for eff in allEffects: 
        for proc in psutil.process_iter():
            if proc.name() == eff:
                print(proc)
                proc.kill()
                os.kill(proc.pid, signal.SIGKILL)

@app.route('/')
@app.route('/home')
def index():
    clearEffects()
    return render_template("index.html",
                        title = 'Home' )

@app.route('/ef/<effect_name>')
def start_effect(effect_name=None):
    print('-new eff->' + effect_name)
    print('-old eff->' + app.config['curr_effect'])
    print((effect_name != app.config['curr_effect']))
    if (effect_name != app.config['curr_effect']):
        clearEffects()
        app_name = effect_name
        app.config["curr_effect"] = app_name
        cmd = root_dir + "/static/effects/" + app_name
        get_exitcode_stdout_stderr(cmd);

    return jsonify(status = 'success')

def group_effects():
    app_name = 'everloop_demo'
    app.config["curr_effect"] = app_name
    cmd = root_dir + "/static/effects/" + app_name
    get_exitcode_stdout_stderr(cmd);
    sleep(4000)
    clearAllEffects()
    sleep(2000)

    app_name = 'arc_demo'
    app.config["curr_effect"] = app_name
    cmd = root_dir + "/static/effects/" + app_name
    get_exitcode_stdout_stderr(cmd);
    sleep(4000)
    clearAllEffects()
    sleep(2000)
    
    app_name = 'direction_of_arrival_demo'
    app.config["curr_effect"] = app_name
    cmd = root_dir + "/static/effects/" + app_name
    get_exitcode_stdout_stderr(cmd);
    sleep(4000)
    clearAllEffects()
    sleep(2000)

    app_name = 'mic_energy'
    app.config["curr_effect"] = app_name
    cmd = root_dir + "/static/effects/" + app_name
    get_exitcode_stdout_stderr(cmd);
    sleep(4000)
    clearAllEffects()
    sleep(2000)

@app.route('/cycle')
def cysle_effects():
    clearAllEffects();
    '''
    if ( app.config['start_cycle'] == True ):
        app.config['start_cycle'] = False
        print("CYCLE_STOPPED")
    else:
        app.config['start_cycle'] = True
        print("CYCLE_STARTED")
    
    while (app.config['start_cycle'] == True):
        group_effects()
        sleep(25000)
    '''    
        

@app.route('/voice-record/')
def voice_record():
    clearEffects()
    print('RUN RECORDER ')
    '''
    clearEffects()
    app_name = 'micarray_recorder'
    if (app_name != app.config['curr_effect']):
        app.config["curr_effect"] = app_name
        cmd = '.' + root_dir + '/static/music/' + app_name
        print('RUN RECORDER ' + cmd)
        get_exitcode_stdout_stderr(cmd)
        
        sleep(12000)
        
        file_name = 'channel_0'
        wav_file = music_dir + '/'+file_name+'.wav'
        cmd = 'sox -r 16000 -c 1 -e signed -b 16 ' + music_dir + '/mic_16000_s16le_channel_0.raw ' + wav_file
        get_exitcode_stdout_stderr(cmd)
        
        cmd = 'lame --preset insane ' + wav_file
        get_exitcode_stdout_stderr(cmd)

        sleep(3000)

    music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
    music_files_number = len(music_files)
    return render_template("index.html",
                        title = 'Home',
                        music_files_number = music_files_number,
                        music_files = music_files)    
        '''
@app.route('/play/<filename>')
def song(filename):
    return render_template('play.html',
                        title = filename,
                        music_file = filename)

def sounds_cleaner():
    #while (true) monitoring sounds dir
    pass

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
