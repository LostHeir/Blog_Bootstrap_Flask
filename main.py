from flask import Flask, render_template
import requests

app = Flask(__name__)
blog_data = requests.get('https://api.npoint.io/88c2c1f644ef334058be').json()


@app.route('/')
def home():
    return render_template("index.html", blog_data=blog_data)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<int:post_id>')
def post(post_id):
    requested_post = None
    for blog_post in blog_data:
        if post_id == blog_post['id']:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
