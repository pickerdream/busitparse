import gettable
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import urlparse

app = Flask(__name__)
# Limiter settings
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.route('/timetable.json', methods=['GET'])
def get_timetable():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "URL parameter is required"}), 400
    if not gettable.is_valid_url(target_url):
        return jsonify({"error": "URL parameter is invaild"}), 400
    else:
        return jsonify(gettable.main(target_url))

if __name__ == '__main__':
    app.run(debug=True, port=3000)