from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
from remixer import main 
import shutil


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'msharda50_be21@thapar.edu'
app.config['MAIL_PASSWORD'] = '4zWHcndLm4Pc6SJ'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


def remixer(n, singer, duration, output_file='output.mp3'):
    print(n, singer, duration)
    main(n=n, sec=duration, singer=singer, output_name=output_file)
    pass


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=["POST"])
def handleForm():
    if request.method == "POST":
            try:
                singer = request.form['singer']
                n = request.form['num_videos']
                duration = request.form['duration']
                email = request.form['email']
                print(singer, n, duration, email)
                remixer(n, singer, duration)
                send_email(email)

            except Exception as e:
                print(e)
                return render_template('error.html')
    return render_template('success.html')


def zip_file(folder_path, output_path):
    try: 
        # print(folder_path)
        # print(os.getcwd())
        archived = shutil.make_archive(output_path, 'zip', folder_path)
    except Exception as e:
        raise Exception("Problem in zipping file: ", e)

def send_email(email):
    try:
        body = "Thank you for using remixer app. Here are your results. Sent by: Mukul Sharda Roll no: 102197016"
        msg = Message("Results:", body=body, sender="msharda50_be21@thapar.edu", recipients=[email])
        
        path = os.path.join(os.getcwd(), 'results')

        zip_file(path, os.getcwd())
        with app.open_resource("output.zip") as fp:  
            msg.attach("output.zip", "application/pdf", fp.read()) 
        mail.send(msg)
        # print("sent email.")
    except Exception as e:
        raise Exception("Problem in sending email: ", e)

if __name__ == "__main__":
    app.run(debug=True) 
