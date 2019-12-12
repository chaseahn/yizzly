#!/usr/bin/env python3


import os
import time

from flask import Flask, render_template, request, url_for, redirect, session
from flask_mail import Mail, Message

from werkzeug.utils import secure_filename

from .controllers.private import subcontroller as private_sub
from .models.model import User
from .extension.security import hasher

controller = Flask(__name__, instance_relative_config=True)
controller.config.from_pyfile('config.py')
controller.secret_key = controller.config['SECRET_KEY']
controller.upload_folder = controller.config['UPLOAD_FOLDER']
controller.allowed_extensions = controller.config['ALLOWED_EXTENSIONS']

controller.register_blueprint(private_sub)

# set up Flask_Mail Instance
mail = Mail(controller)


@controller.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('public/login.html')
    elif request.method == 'POST':
        if request.form['post_button'] == 'Login':
            un = request.form['username']
            pw = hasher(request.form['password'])
            #check login and serve to main page
            try:
                with User(username=un,password=pw) as user:
                    if user.login(pw):
                        #send to mainpage
                        session['username'] = user.username
                        session['pk'] = user.pk
                        return redirect('private/index')
            except TypeError as e:
                print(e)

    else:
        pass

@controller.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        # welcome to register page
        return render_template('public/register.html')

    elif request.method == 'POST':

        un = request.form['username']
        pw = request.form['password']

        with User(username=un,password=pw) as user:
            print('checking user....')
            if user.username_exist(un):
                return render_template(
                    'public/register.html', 
                    message="Username exists." 
                    )
            elif pw == request.form['confirm_password']:
                user.create_user(un, hasher(pw))
                return redirect('/')
            else:
                return render_template(
                    'public/register.html', 
                    message="Passwords do not match." 
                    )
    else:
        pass

@controller.errorhandler(404)
def not_found(error):
    return render_template('public/404.html')

