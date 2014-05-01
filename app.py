from flask import Flask, jsonify
import gardner_scraper
import peabody_scraper
import harvard_art_scraper

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/gardner")
def scrape_gardner():
    return jsonify(gardner_scraper.scrape())

@app.route("/harvard")
def scrape_harvard():
	return jsonify(harvard_art_scraper.scrape())

@app.route("/peabody")
def scrape_peabody():
	return jsonify(peabody_scraper.scrape()) 

if __name__ == "__main__":
    app.run(debug=True, port=7000)
