# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:45:05 2016

@author: yiyuezhuo
"""

from flask import Flask,render_template,send_from_directory,request
import sympy_wrap
import os
import json

CUR_DIR = os.path.realpath(os.path.dirname(__file__))

static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")


app = Flask(__name__,template_folder=os.path.join(CUR_DIR,'app'))
#app.register_routes_to_resources(static_folder_root)

#app._static_folder=os.path.join(CUR_DIR,'app')
php={}

@app.route('/')
def hello_world():
    print("f**k")
    return render_template('index.html')
    
@app.route('/js/<path:path>')
def static_js(path):
    return send_from_directory(os.path.join(static_folder_root,'js'),path,cache_timeout = 0)
    
@app.route('/css/<path:path>')
def static_css(path):
    return send_from_directory(os.path.join(static_folder_root,'css'),path,cache_timeout = 0)

    
@app.route('/solve',methods=['GET','POST'])
def solve():
    #return json.dumps({1:2,2:3})
    #form=dict(request.form)
    #print('data:')
    print('request.data')
    print(request.data)
    print('request.get_json()')
    print(request.get_json())
    #form=request.get_json()
    print('--------------')
    print('request.form')
    print(request.form)
    #print(type(request.form))
    print('request.args')
    print(request.args)
    print('request')
    print(request)
    print('request.values')
    print(request.values)
    print('request.path')
    print(request.path)
    form=dict(request.form)
    print('dict(request.form)')
    print(form)
    #ugly hack,what the fuck d3.js and flask
    form=json.loads(list(dict(request.form).keys())[0])
    print('form')
    print(form)
    rd=php['system'].solve(form)
    print('rd')
    print(rd)
    return json.dumps(rd)
    
@app.route('/load')
def load():
    php['system']=sympy_wrap.load()
    return ''
    


def run():
    app.run(debug=True)
    
