from flask import Flask, render_template, request
import smtplib

app = Flask(__name__)

"""
to start testing mail server in terminal, use the following command:
python3 -m smtpd -c DebuggingServer -n localhost:1025
the terminal will then sit and listen for incoming messages
"""


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        recipient = [request.form["recipient"]]
        recipient_name = request.form["rname"]
        body = request.form["body"]
        body = f"Hello {recipient_name},\n{body}"
        subject = "Spike-prototype test"
        msg = f"Subject: {subject}\n\n{body}"

        # don't do this in production, can store as envirnment variables
        # and retrieve with os module
        sender = "371emailTestBot@gmail.com"
        sender_password = "thisistestbot371!"

        # create connection to mail server (current notation using with means
        # we do not need server.quit() method to close connection)
    
        # with smtplib.SMTP("smtp.gmail.com", 587) as server:
        with smtplib.SMTP("localhost", 1025) as server:
            # server.ehlo()           # identifies us with mail server
            # server.starttls()       # encrypt traffic
            # server.ehlo()
            # server.login(sender, sender_password)
            server.sendmail(sender, recipient, msg)
        return f"email successfully sent to {recipient}"
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
