from flask import Flask, jsonify
from scrapers import cordova, gardner, harvard_art, mit_list, mfa, peabody, rose

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/gardner")
def scrape_gardner():
    results = {"results": gardner.scrape()}
    return jsonify(results)

@app.route("/harvard")
def scrape_harvard():
    results = {"results": harvard_art.scrape()}
    return jsonify(results)

@app.route("/peabody")
def scrape_peabody():
    results = {"results": peabody.scrape()}
    return jsonify(results) 

@app.route("/mfa")
def scrape_mfa(): 
	results = {"results": mfa.scrape()}
	return jsonify(results)

@app.route("/rose")
def scrape_rose(): 
	results = {"results": rose.scrape()}
	return jsonify(results)

@app.route("/cordova")
def scrape_cordova(): 
	results = {"results": cordova.scrape()}
	return jsonify(results)

@app.route("/list")
def scrape_list(): 
	results = {"results": mit_list.scrape()}
	return jsonify(results)