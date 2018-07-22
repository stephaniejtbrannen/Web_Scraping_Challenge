# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# create instance of Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    mars_news = mission_to_mars.scrape_news()
    feature_img = mission_to_mars.scrape_featured_img()
    mars_weather = mission_to_mars.scrape_weather()
    facts_table = mission_to_mars.scrape_fun_fact()
    hemisphere_image_urls = mission_to_mars.scrape_hemispere_images()
    # Store results into a dictionary
    mars_data = {
        "news_title": mars_news["news_title"],
        "news_content": mars_news["news_content"],
        "featured_image_url": feature_img,
        "mars_weather": mars_weather,
        "fact_table" : facts_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }
    mongo.db.collection.remove()
    # Insert mars_db into database
    mongo.db.collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
