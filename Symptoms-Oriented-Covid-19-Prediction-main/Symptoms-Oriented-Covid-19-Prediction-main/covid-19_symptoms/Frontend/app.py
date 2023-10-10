from flask import Flask, render_template, request, redirect, url_for, session
from tensorflow.keras.models import load_model
from flask_mysqldb import MySQL
import numpy as np

app = Flask(__name__)
app.secret_key = 'covid'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "March981*"
app.config['MYSQL_DB'] = 'covid19'

mysql = MySQL(app)

model = load_model("project/models/ArtificialNeuralNetwork_model.h5")

class_labels = ['NORMAL', 'COVID19']


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("select * from users where email=%s and password=%s", (email, pwd))
        user = cur.fetchone()
        if user:
            session['logged_in'] = True
            session['user'] = user
            # return render_template('home.html', user=session['user'][1])
            return redirect(url_for('home'))
        else:
            msg = 'Invalid Login Details Try Again'
            return render_template('login.html', msg=msg, email=email)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        Password = request.form['Password']
        last_name = request.form['Last_name']
        sex = request.form['gender']
        city = request.form['city']
        country = request.form['country']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        mail_user = cursor.fetchone()
        if not mail_user:
            cursor.execute('INSERT INTO users(name,last_name,gender,email,password,city,country)'
                           ' VALUES(%s,%s,%s,%s,%s,%s,%s)', (name, last_name, sex, email, Password, city, country))
            mysql.connection.commit()
            cursor.close()
            if sex == 'Male':
                msg1 = " Hello mr." + name + " !! U Can login Here !!!"
                return render_template('login.html', msg=msg1, email=email)
            else:
                msg1 = " Hello ms." + name + " !! U Can login Here !!!"
                return render_template('login.html', msg=msg1, email=email)

        msg2 = "This Email Id is already Registered"
        return render_template('register.html', msg1=msg2)

    return render_template('register.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'user' in session:
        return render_template("home.html", user=session['user'][1])
    return render_template('login.html')


@app.route('/password', methods=['POST', 'GET'])
def password():
    if 'user' in session:
        if request.method == 'POST':
            current_pass = request.form['current']
            new_pass = request.form['new']
            verify_pass = request.form['verify']
            email = session['user'][4]
            cur = mysql.connection.cursor()
            cur.execute("select password from users where email=%s", (email,))
            user = cur.fetchone()
            user = user[0]
            if user:
                if user == current_pass:
                    if new_pass == verify_pass:
                        msg1 = 'Password changed successfully'
                        cur.execute("UPDATE users SET password = %s WHERE password=%s", (new_pass, current_pass))
                        mysql.connection.commit()
                        return render_template('password.html', msg1=msg1, user=session['user'][1])
                    else:
                        msg2 = 'Re-entered password is not matched'
                        return render_template('password.html', msg2=msg2, user=session['user'][1])
                else:
                    msg3 = 'Incorrect password'
                    return render_template('password.html', msg3=msg3, user=session['user'][1])
            else:
                msg3 = 'Incorrect password'
                return render_template('password.html', msg3=msg3, user=session['user'][1])
        return render_template('password.html', user=session['user'][1])
    return render_template('login.html')


@app.route('/graphs', methods=['POST', 'GET'])
def graphs():
    return render_template("graphs.html", user=session['user'][1])


@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    return render_template("prediction.html", user=session['user'][1])


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        sub = request.form['subject']
        msg = request.form['message']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email FROM contacts WHERE email=%s", (email,))
        mail_user = cursor.fetchone()
        if not mail_user:
            cursor.execute('INSERT INTO contacts(name,email,subject,message)'
                           ' VALUES(%s,%s,%s,%s)', (name, email, sub, msg))
            mysql.connection.commit()
            cursor.close()
            return render_template("contact.html", msg='Thankyou for contacting with us..', user=session['user'][1])
        return render_template("contact.html", msg='Your request is already taken.', user=session['user'][1])
    return render_template("contact.html", user=session['user'][1])


@app.route('/predict', methods=['POST'])
def predict():
    ui = []

    if request.method == 'POST':
        ui.append(int(request.form['bp']))
        ui.append(int(request.form['fv']))
        ui.append(int(request.form['dc']))
        ui.append(int(request.form['st']))
        ui.append(int(request.form['rn']))
        ui.append(int(request.form['am']))
        ui.append(int(request.form['cld']))
        ui.append(int(request.form['hc']))
        ui.append(int(request.form['hd']))
        ui.append(int(request.form['db']))
        ui.append(int(request.form['ht']))
        ui.append(int(request.form['ft']))
        ui.append(int(request.form['gi']))
        ui.append(int(request.form['at']))
        ui.append(int(request.form['cwcp']))
        ui.append(int(request.form['alg']))
        ui.append(int(request.form['vpep']))
        ui.append(int(request.form['fwipep']))
        ui.append(int(request.form['wm']))
        ui.append(int(request.form['sfm']))

        print("its come to 1 if")
    print(ui)

    l = []
    for i in ui:
        l.append(i)
    l1 = []
    l1.append(l)
    print(l1)
    # rfc = pickle.load(open('models/AdaBoost_model.pkl', 'rb'))

    result = model.predict(l1)

    class_name = np.argmax(result[0])
    class_label = class_labels[class_name]
    probability = result[0][class_name]
    probability = f'Probability: {probability * 100:.2f}%'
    return render_template('result.html', res=class_label, b=probability, user=session['user'][1])


@app.route('/logout')
def logout():
    if 'user' in session:
        # session.clear()
        session.pop('user')
        msg = 'You are now logged out', 'success'
        return redirect(url_for('login', msg=msg))
    return render_template('login.html')
