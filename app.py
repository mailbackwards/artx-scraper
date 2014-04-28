from flask import Flask, jsonify
import gardner_scraper
import peabody_scraper
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/gardner", method=['GET'])
    return gardner_scraper.scrape()

if __name__ == "__main__":
    app.run()