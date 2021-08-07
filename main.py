from flask import Flask, render_template, request
import requests
import smtplib
import os

my_email = os.environ['MY_EMAIL']
password = os.environ['MY_PASSWORD']

app = Flask(__name__)
blog_data = requests.get('https://api.npoint.io/88c2c1f644ef334058be').json()


@app.route('/')
def home():
    return render_template("index.html", blog_data=blog_data)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", method="get")
    elif request.method == 'POST':
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=os.environ['MY_ENDMAIL'],
                msg=f"Subject:New Message - Blog\n\nName: {request.form['name']} \nEmial: {request.form['email']}"
                    f" \nPhone: {request.form['phone']} \nMessage: {request.form['message']}"
            )
        return render_template("contact.html", method="post")


@app.route('/post/<int:post_id>')
def post(post_id):
    requested_post = None
    for blog_post in blog_data:
        if post_id == blog_post['id']:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
