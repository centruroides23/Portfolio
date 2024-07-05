# ----------------------------------------------- Modules Declaration ------------------------------------------------ #
import os
import asyncio
import aiosmtplib
import bleach
import datetime as dt
from flask import Flask, render_template, url_for, redirect, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_forms import ContactForm
from flask_ckeditor import CKEditor


# ---------------------------------------------- Variable Declaration ------------------------------------------------ #
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
CURRENT_YEAR = dt.datetime.now().year


# --------------------------------------------- Application Declaration ---------------------------------------------- #
app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = "static/files"


# ------------------------------------------------ Function Declaration ---------------------------------------------- #
async def send_email_async(msg):
    async with aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587) as connection:
        await connection.login(USERNAME, PASSWORD)
        await connection.sendmail(USERNAME, USERNAME, msg)


# ---------------------------------------------------- App Routes ---------------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        phone_number = form.phone.data
        message = form.message.data
        full_email = (f"Subject: Message from Personal Website\n\n{message.encode('utf-8')}\n\n\n"
                      f"From: {username}\nEmail: {email}\nPhone Number: {phone_number}")
        asyncio.run(send_email_async(full_email))
        return redirect(url_for("receive_data"))
    return render_template("index.html",
                           form=form,
                           year=str(CURRENT_YEAR))


@app.route("/receive_data")
def receive_data():
    return render_template("receive_data.html")


@app.route('/certification_tables/<certification_name>')
def certification_tables(certification_name):
    certification_name = certification_name
    return render_template('certification_tables.html',
                           certification_name=certification_name)


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],
                               path=filename,
                               as_attachment=True)


# ------------------------------------------------ Run the Application ----------------------------------------------- #
if __name__ == "__main__":
    app.run(debug=False, port=5000)