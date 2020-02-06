#!/usr/bin/env python3


import os
import requests

from flask import Blueprint,render_template,request,redirect,url_for,session,flash, current_app, send_from_directory
from time  import gmtime,strftime
from werkzeug.utils import secure_filename

from ..models.model import User
from ..models.app import *

subcontroller = Blueprint('private',__name__)

ALLOWED_EXTENSIONS = set(['edl'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@subcontroller.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        user = User({'username': session['username'], 'pk': session['pk']})
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

        elif request.form['post_button'] == 'TRANSCRIBE':
            flash('Not active')
            return redirect(url_for('private.index'))
        else:
            print('else hit')
            pass
    else:
        pass

@subcontroller.route('/log',methods=['GET','POST'])
def log():
    if request.method == 'GET':
        user = User({'username': session['username'], 'pk': session['pk']})
        return render_template('private/log.html',
            title="Footage Log",
            username=user.username,
            message="Let's log some clips!"
            )
    elif request.method == 'POST':
        user_input = request.form['info']
        dmm = DMMLogger(log_input=user_input)
        clip_object = dmm.create_clip_object()
        #bring over clip info
        session['clip'] = clip_object
        # log_str = f"Rating: {clip_object['rating']} | {clip_object['clip_type']}\
        #         | Info: {clip_object['description']} [Q{clip_object['period']}\
        #             {clip_object['time']}] Players: {clip_object['players']}"
        return redirect(url_for('private.log_commit'))
    else:
        pass

@subcontroller.route('/log-commit',methods=['GET','POST'])
def log_commit():
    if request.method == 'GET':
        clip = session['clip']
        print(clip)
        user = User({'username': session['username'], 'pk': session['pk']})
        return render_template('private/log_commit.html',
            title="Footage Log: Commit",
            username=user.username,
            clip=clip,
            message="Save this clip for later! :)"
            )
    elif request.method == 'POST':
        if request.form['post_button'] == 'COPY INFO':
            print('hi')
            return ('', 204)
        else:
            #save clip
            return redirect(url_for('private.clip_success'))
    else:
        pass

@subcontroller.route('/clip-success',methods=['GET','POST'])
def clip_success():
    if request.method == 'GET':
        return render_template('private/clip_success.html')
    elif request.method == 'POST':
        pass
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