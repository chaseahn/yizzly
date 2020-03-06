#!/usr/bin/env python3


import os
import time

from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_mail import Mail, Message

from werkzeug.utils import secure_filename

from .controllers.private import subcontroller as private_sub
from .models.model import User
from .extension.security import *

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
                        session['logged_in'] = True
                        return redirect('/index')
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

        #store user information into session object
        #can be accessed by calling session['NEW_USER'][attr]
        session['NEW_USER'] = {
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email'],
            'code': randint(6)
        }

        #Check for User Existance
        user = User()
        if user.exists(session['NEW_USER']['username']):
            return render_template(
                'public/register.html', 
                message="Username exists." 
                )
        else:
            return redirect('/verify')
    else:
        pass

@controller.route('/verify',methods=['GET','POST'])
def verify():
    #get new_user session object
    new_user = session.get('NEW_USER')
    print(new_user['code'])
    if request.method == 'GET':
        #verifincation page
        return render_template('public/verify.html')

    elif request.method == 'POST':
        #match the session code with the user input
        if request.form['code'] == new_user['code']:
            
            with User(
                username=new_user['username'],
                password=new_user['password']
                ) as user:
                
                user.create_user(
                    new_user['username'],
                    hasher(new_user['password']),
                    new_user['email']
                )

                return redirect('/success')
        else:
            flash("Incorrect code. Please Try again.")
            return render_template('public/verify.html')

    else:
        pass

@controller.route('/logout',methods=['GET'])
def logout():
    session.pop('logged_in')
    return redirect(url_for('login'))

@controller.route('/success',methods=['GET'])
def success():
    return render_template('public/success.html')

@controller.errorhandler(404)
def not_found(error):
    return render_template('public/404.html')

