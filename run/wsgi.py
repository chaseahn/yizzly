#!/bin/usr/env python3

from flask import Flask

from src import controller

controller.run('0.0.0.0', debug=True)