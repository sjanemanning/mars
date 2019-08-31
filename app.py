from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrapemars
import os


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb+srv://smanning:oklahoma10@cluster0-5ymef.mongodb.net/test")


@app.route("/")
def home(): 

    
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape(): 

    mars_info = mongo.db.mars_info
    mars_data = scrapemars.scrape_mars_news()
    mars_data = scrapemars.scrape_mars_image()
    mars_data = scrapemars.scrape_mars_facts()
    mars_data = scrapemars.scrape_mars_weather()
    mars_data = scrapemars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)