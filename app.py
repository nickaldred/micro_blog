from flask import Flask, render_template, request, redirect
import datetime
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

load_dotenv()

ca = certifi.where()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"), tlsCAFile=ca)
    app.db = client.Microblog

    


    @app.route("/", methods = ["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )

            for entry in app.db.entries.find({})

        ]
        return render_template("home.html", entries=entries_with_date)

    @app.route("/recent", methods = ["GET", "POST"])
    def recent():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )

            for entry in app.db.entries.find({})

        ]
        return render_template("recent.html", entries=entries_with_date)

    @app.route("/portfolio")
    def portfolio():
        return redirect("https://nickaldred.com/")

    @app.route("/github")
    def github():
        return redirect("https://github.com/nickaldred/micro_blog")


    return app

app = create_app()

app.run(debug=True, host='0.0.0.0', port=81)