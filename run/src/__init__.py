#!/usr/bin/env python3


import os
import time

from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

#from .controllers.private import subcontroller as private_sub
from .models.model import User


UPLOAD_FOLDER = '/Users/ahn.ch/Projects/shoe_data/run/src/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) #might have to change for videos 

controller = Flask(__name__)

controller.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
controller.secret_key = 'SUPER-DUPER-SECRET'


# controller.register_blueprint(private_sub)

@controller.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('public/login.html')
    elif request.method == 'POST':
        if request.form['post_button'] == 'Login':
            un = request.form['username']
            pw = request.form['password']
            #check login and serve to main page
            try:
                with User(username=un,password=pw) as u:
                    if u.login(pw):
                        #send to mainpage
                        print("DWKJNAWBHDAWBKHAWjkaknjwnjb")
                        # return redirect('/main')
            except TypeError as e:
                print(e)

    else:
        pass

@controller.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('public/register.html')
    elif request.method == 'POST':
        print("start register")
        un = request.form['username']
        pw = request.form['password']
        #check login and serve to index
        #check for unique USERNAME
        #TODO make registration flow
        with User(username=un,password=pw) as u:
            if u.check_username():
                return render_template(
                    'public/register.html', 
                    message="Username Exists" )
            else:
                #TODO ad
                pass
    else:
        pass

