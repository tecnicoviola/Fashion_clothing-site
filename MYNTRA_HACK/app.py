import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from idiot import search
from search_cosine_similarity  import cosine_similarity_T
import pandas as pd
import numpy as np
import random
# from asr_myntra import speech_text


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn 


app = Flask(__name__)

@app.route('/')
def index():
 return render_template("home.html")



# @app.route('/voice',methods=['POST'])
# def voice():
#     query = request.form['voice_query'].lower()
#     tokens = query.split()
#     print(tokens)
#     if "north" in tokens:
#         if "east" in tokens or "eastern" in tokens:
#             return redirect('http://localhost:5000/region/north-east')
#         else:
#             return redirect('http://localhost:5000/region/north')
#     elif "west" in tokens or "western" in tokens:
#         return redirect('http://localhost:5000/region/western')
#     elif "south" in tokens or "southern" in tokens:
#         return redirect('http://localhost:5000/region/south') 
#     elif "east" in tokens or "eastern" in tokens:
#         return redirect('http://localhost:5000/region/east')
#     elif "northeastern" in tokens:
#         return redirect('http://localhost:5000/region/north-east')
    
#     return render_template("home.html")


def prodDetails(id):
    df = pd.read_csv('Myntra_dataset.csv')
    # print(type(df['uniq_id'][0]))
    details = pd.DataFrame()
    details = df[df['uniq_id'] == id]
    print("One Product")
    print(details)
    for i in details.index:
        details.loc[i,'price'] = random.randint(500, 5000)
    return details


@app.route('/voice',methods=['POST'])
def voice():
    query = request.form['voice_query'].lower()
    tokens = query.split()
    print(tokens)
    if "north" in tokens or "northern" in tokens:
        if "east" in tokens or "eastern" in tokens:
            return redirect('http://localhost:5000/region/north-east')
        else:
            return redirect('http://localhost:5000/region/north')
        return render_template("home.html")        
    elif "west" in tokens or "western" in tokens:
        return redirect('http://localhost:5000/region/western')
        return render_template("home.html") 
    elif "south" in tokens or "southern" in tokens:
        return redirect('http://localhost:5000/region/south') 
        return render_template("home.html") 
    elif "east" in tokens or "eastern" in tokens:
        return redirect('http://localhost:5000/region/east')
        return render_template("home.html") 
    elif "northeastern" in tokens:
        return redirect('http://localhost:5000/region/north-east')
        return render_template("home.html") 
    elif "home" in tokens or "homepage" in tokens:
        return redirect('http://localhost:5000/')
        return render_template("home.html")         
    else:    
        print(query)
        dataframe = cosine_similarity_T(10,query)
        print(dataframe)
        return render_template("results.html",data=dataframe)
    return render_template("results.html",data=dataframe)
    


@app.route('/add/<string:id>/<string:q>',methods=['POST'])
def add(id,q):
    qty = int(q)
    query = request.form['add_query'].lower()

    details = prodDetails(id)
    print(query)
    tokens = query.split()
    s = []
    for t in tokens:
        try:
            s.append(int(t))
        except ValueError:
            pass
    if "add"  in tokens:
        return render_template("add.html",data=details, qty=qty)
    elif "quantity" in tokens and s:
        qty=s[0]
        return render_template("add.html",data=details, qty=qty)
    elif "place" in tokens or "complete" in tokens or "done" in tokens or "order" in tokens:
        return render_template("order.html",data=details,qty=qty)


    return render_template("single.html",data=details,qty=1)



@app.route('/product/<string:id>',methods=['GET'])
def giveProd(id):
    details = prodDetails(id)
    return render_template("single.html",data=details,qty=1)




    

@app.route('/region/<string:region>',methods=['GET'])
def north(region):
    df = search(region)
    print(df)
    return render_template("results_region.html",data=df)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
