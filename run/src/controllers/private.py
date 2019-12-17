#!/usr/bin/env python3


import os
import requests

from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from time  import gmtime,strftime

from ..models.model import User
from ..models.app import DMMLogger

subcontroller = Blueprint('private',__name__)



@subcontroller.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        user = User({'username': session['username'], 'pk': session['pk']})
        return render_template('private/index.html')
    elif request.method == 'POST':
        pass
    else:
        pass

@subcontroller.route('/log',methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('private/log.html')
    elif request.method == 'POST':
        clip_input = str(request.form['info'])
        converted_input = DMMLogger(clip_input)
        return render_template(
            'private/log.html', 
            message=converted_input
            )
    else:
        pass