#!/usr/bin/env python3


import os
import requests
import pyperclip

from flask import Blueprint,render_template,request,redirect,url_for,session,flash, current_app, send_from_directory
from time  import gmtime,strftime
from werkzeug.utils import secure_filename

from ..models.model import *
from ..models.app import *

subcontroller = Blueprint('private',__name__)

ALLOWED_EXTENSIONS = set(['edl'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@subcontroller.route('/index',methods=['GET','POST'])
def index():
    user = User({'username': session['username'], 'pk': session['pk']})
    if request.method == 'GET':
        session['clip_was_logged'] = False
        return render_template(
            'private/index.html', 
            title="Rooks Portal",
            username=user.username,
            message="What would you like to do today?"
            )
    elif request.method == 'POST':
        if request.form['post_button'] == 'CONVERT':

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('private.index'))

            file = request.files['file']

            print("Current File: "+str(file))
            print("Filename: "+str(file.filename))

            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('private.index'))

            if file and allowed_file(file.filename):
                #secure_filename check
                filename = secure_filename(file.filename)
                uploads = current_app.config['UPLOAD_FOLDER']
                file_path = os.path.join(uploads, filename)
                #save file to server
                print("Saving to " + str(file_path))
                file.save(file_path)
                print("Saved")
                #read file from server
                with open(file_path) as user_file:
                    #convert EDL 
                    edl = EDL(path=file_path,name=filename,frame_rate='29.97')
                    edl.execute()
                os.remove(file_path)
                directory = os.path.join(current_app.root_path, uploads)
                print(directory)
                csv_file = filename.split('.')[0]+'.csv'
                return send_from_directory(
                    directory=uploads, 
                    filename=csv_file,
                    as_attachment=True)
                # os.remove(directory+csv_file)
        else:
            pass
    else:
        pass

@subcontroller.route('/log',methods=['GET','POST'])
def log():
    user = User({'username': session['username'], 'pk': session['pk']})
    if request.method == 'GET':
        if session['clip_was_logged']:
            # only if directed from log-commit with new clip
            # show same template with last logged clip
            # allow users to make edits to PREV clip  
            return render_template('private/log.html',
                title="Footage Log",
                username=user.username,
                message="Successfully logged! Way to go!",
                placeholder="Start a new clip.",
                previous_clip=session['clip'],
                home_team = session['last_clip_logged']['home_team'],
                away_team = session['last_clip_logged']['away_team']
                )
        else:
            # standard log template
            return render_template('private/log.html',
                title="Footage Log",
                username=user.username,
                message="Let's log some clips!",
                placeholder="Copy & paste the clip information from the DMM to here."
                )
        
    elif request.method == 'POST':
        # create a clip
        # redirect to log_commit for inspection and submission
        user_input = request.form['info']
        dmm = DMMLogger(log_input=user_input)
        clip_object = dmm.create_clip_object()
        #bring over clip info
        session['clip'] = clip_object
        return redirect(url_for('private.log_commit'))
    else:
        pass

@subcontroller.route('/log-commit',methods=['GET','POST'])
def log_commit():
    if request.method == 'GET':
        clip_object = session['clip']
        user = User({'username': session['username'], 'pk': session['pk']})
        return render_template('private/log_commit.html',
            title="Footage Log: Commit",
            username=user.username,
            clip=clip_object,
            message="Save this clip for later! :)"
            )
    elif request.method == 'POST':
        # Check for includes....
        # FIXME maybe consider radio?
        check_one = str(request.form.get('check_1'))
        check_two = str(request.form.get('check_2'))
        check_three = str(request.form.get('check_3'))
        includes = ', '.join([check_one,check_two,check_three])

        final_clip = {
            'game_id': request.form.get('game_id'),
            'home_team': request.form.get('home_team'),
            'away_team': request.form.get('away_team'),
            'game_date': request.form.get('game_date'),
            'rating': request.form.get('rating'),
            'type': request.form.get('type'),
            'includes': includes,
            'players': request.form.get('players'),
            'description': request.form.get('description'),
            'quarter': request.form.get('quarter'),
            'time': request.form.get('time')
        }

        #TODO make string cleaner
        log_str = f"Rating: {final_clip['rating']} // Clip Type: {final_clip['type']}, {final_clip['includes']} [Info] {final_clip['description']} // Players: {final_clip['players']} [Q{final_clip['quarter']} {final_clip['time']}]"

        # OS Copy function for markers in Premerie
        if request.form['post_button'] == 'COPY INFO':
            """ OS COPY LOG STR """
            pyperclip.copy(log_str)
            return ('', 204)
        # commit the clip to the database
        # turn session['clip_was_logged'] into True
        # init session['clip_was_logged'] into False at /index
        else:
            clip = Clips()
            clip.save_clip(final_clip)
            session['clip_was_logged'] = True
            session['last_clip_logged'] = final_clip
            return redirect(url_for('private.log'))
    else:
        pass

@subcontroller.route('/cuesheet',methods=['GET','POST'])
def cuesheet():
    user = User({'username': session['username'], 'pk': session['pk']})
    if request.method == 'GET':
        return render_template('private/cuesheet.html', 
            title="Cuesheet",
            username=user.username,
            message="Let's make a cuesheet!")
    #TODO make more dynamic
    elif request.method == 'POST':
        filename = 'name'
        user_input = request.form['info']
        print(user_input)
        uploads = current_app.config['UPLOAD_FOLDER']
        cue = CueSheet(user_input=user_input, name=filename)
        cue.convert_cues_to_csv()
        directory = os.path.join(current_app.root_path, uploads)
        csv_file = filename+'.csv'
        return send_from_directory(
            directory=uploads, 
            filename=csv_file,
            as_attachment=True)
    else:
        pass

@subcontroller.route('/add-player',methods=['GET','POST'])
def add_player():
    user = User({'username': session['username'], 'pk': session['pk']})
    if request.method == 'GET':
        api = NBAapi()
        api.find_matching_players(fname='rj', lname='barrett')
        return ('', 204)