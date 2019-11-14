#!/usr/bin/env python3


import os
import time

from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

#from .controllers.private import subcontroller as private_sub
#from .models.model import 


UPLOAD_FOLDER = '/Users/ahn.ch/Projects/shoe_data/run/src/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) #might have to change for videos 

controller = Flask(__name__)

controller.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
controller.secret_key = 'SUPER-DUPER-SECRET'


# controller.register_blueprint(private_sub)



@controller.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('public/index.html')
    elif request.method == 'POST':
        pass
    else:
        pass