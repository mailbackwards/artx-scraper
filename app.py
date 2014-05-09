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
    results = {"results": gardner_scraper.scrape()}
    return jsonify(results)

@app.route("/harvard")
def scrape_harvard():
    results = {"results": harvard_art_scraper.scrape()}
    return jsonify(results)

@app.route("/peabody")
def scrape_peabody():
    results = {"results": peabody_scraper.scrape()}
    return jsonify(results) 

@app.route("/mfa")
def scrape_mfa(): 
	results = {"results": mfa_scraper.scrape()}
	return jsonify(results)

@app.route("/rose")
def scrape_rose(): 
	results = {"results": rose_scraper.scrape()}
	return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=7000)
