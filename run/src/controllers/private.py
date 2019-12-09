#!/usr/bin/env python3


import os
import requests

from bs4 import BeautifulSoup
from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from time  import gmtime,strftime

from ..models.model import User

subcontroller = Blueprint('private',__name__,url_prefix='/private')



@subcontroller.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        user = User({'username': session['username'], 'pk': session['pk']})
        return render_template('private/index.html')
    elif request.method == 'POST':
        pass
    else:
        pass