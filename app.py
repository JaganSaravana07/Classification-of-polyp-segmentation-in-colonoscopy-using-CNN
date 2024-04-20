from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psycopg2
import os
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import sqlite3
from load_data import train  
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import cv2
from PIL import Image


app = Flask(__name__)
app.secret_key ="jbdifgsajdfbdifgs2387622"

database="new.db"
conn=sqlite3.connect(database)
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS user (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS patient_details (userid INTEGER PRIMARY KEY AUTOINCREMENT,Patient_id int, Patient_name TEXT, Patient_age int,Patient_email text,blood_group text,Patient_address text,gender text,Patient_mobile int)")
conn.commit()



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login1', methods=['GET', 'POST'])
def login1():
        return render_template('login_page.html')

images_dir = 'PNG/Original'
masks_dir = 'PNG/Ground Truth'
x_test, y_test = train(images_dir, masks_dir)

profile=[]
email=[]
@app.route('/login', methods=['GET', 'POST'])
def login():
       if request.method=="POST":
            usermail=request.form["usermail"]
            password=request.form["login_password"]
            conn=sqlite3.connect(database)
            cur=conn.cursor()
            cur.execute("select * from user where email=? and password=?",(usermail,password))
            data=cur.fetchone()
            if data:
                  profile.append(data[1])
                  email.append(data[2])
                  return render_template('Dashboard.html')
            else:
                return"password mismatch"
       return render_template('login_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method=="POST":
       username=request.form["username"]
       email=request.form["email"]
       password=request.form["password"]
       confirm_password=request.form["confirm_password"]
       conn=sqlite3.connect(database)
       cur=conn.cursor()
       cur.execute("INSERT INTO user (username, email, password) VALUES (?, ?, ?)", (username, email, password))
       conn.commit()
       return render_template('login_page.html')




@app.route('/userprofile',methods=['GET', 'POST'])
def userprofile():  
    return render_template('user_profile.html',email=email[-1],name=profile[-1])


@app.route('/patientregister',methods=['GET', 'POST'])
def patientregister():
    return render_template('register_page.html')



@app.route('/patientregister1',methods=['GET', 'POST'])
def patientregister1():
        Patient_id=request.form["Patient_id"]
        Patient_name=request.form["Patient_name"]
        Patient_age=request.form["Patient_age"]
        Patient_email=request.form["Patient_email"]
        blood_group=request.form["blood_group"]
        Patient_address=request.form["Patient_address"]
        gender=request.form["gender"]
        Patient_mobile=request.form["Patient_mobile"]
        conn=sqlite3.connect(database)
        cur=conn.cursor()

        cur.execute("INSERT INTO patient_details (Patient_id, Patient_name, Patient_age,Patient_email,blood_group,Patient_address,gender,Patient_mobile) VALUES (?,?,?,?,?,?,?,?)", (Patient_id, Patient_name, Patient_age,Patient_email,blood_group,Patient_address,gender,Patient_mobile))
        conn.commit()
        return render_template('register_page.html')


def dice_coefficient(y_true, y_pred, smooth=1):
        intersection = tf.reduce_sum(tf.abs(y_true * y_pred), axis=-1)
        union = tf.reduce_sum(y_true, axis=-1) + tf.reduce_sum(y_pred, axis=-1)
        return (2. * intersection + smooth) / (union + smooth)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        l=filename[:-4]
        l1=int(l)
        input_image = x_test[l1]
        Predicted_mask_binary = y_test[l1]
        threshold = 0.5  
        loaded_model = load_model('fcn_model.h5', custom_objects={'dice_coefficient': dice_coefficient})
        predicted_mask = loaded_model.predict(np.expand_dims(input_image, axis=0))[0]
        predicted_mask_binary = (predicted_mask > threshold).astype(np.uint8)
        save_dir = 'static/inputimage'
        os.makedirs(save_dir, exist_ok=True)
        input_image_path = os.path.join(save_dir, 'original_image.png')
        plt.imsave(input_image_path, input_image)
        Predicted_mask_path = os.path.join(save_dir, 'Predicted_mask.png')
        area_pixels = np.sum(Predicted_mask_binary[:, :, 0] > 0)
        DPI = 300
        cm_per_pixel = 2.54 / DPI
        area_cm2 = area_pixels * cm_per_pixel**2
        side_length_cm = (area_cm2)**0.5 
        final="{:.2f}".format(side_length_cm)

        plt.imsave(Predicted_mask_path,Predicted_mask_binary[:, :, 0], cmap='gray')
        imag1 = "static/inputimage/original_image.png"
        imag2 = "static/inputimage/Predicted_mask.png"
        Img = cv2.imread(imag1)
        Img1 = cv2.imread(imag2)
        img = cv2.addWeighted(Img, 0.8, Img1, 0.6, 0)
        cv2.imwrite('static/inputimage/final_output.jpg', img)
        return render_template('result.html',length=final)
            


@app.route('/edit', methods=["GET","POST"])
def edit():
    username=request.form["newUsername"]
    newEmail=request.form["newEmail"]
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("UPDATE user SET username=?, email=? WHERE username=?", (username, newEmail, profile[-1]))
    conn.commit()
    return render_template('home.html') 



@app.route('/editprofile', methods=["GET","POST"])
def editprofile():
    return render_template('edit-profile.html')

@app.route('/delete_patient/<int:userid>', methods=['DELETE'])
def delete_patient(userid):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM patient_details WHERE userid=?", (userid,))
        conn.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error deleting patient: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete patient'}), 500



if __name__ == '__main__':
    app.run(debug=False,port=400)
