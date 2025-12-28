import gettable
from flask import Flask, request, jsonify
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

app = Flask(__name__)
@app.route('/timetable.json', methods=['GET'])
def get_timetable():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "URL parameter is required"}), 400
    if not is_valid_url(target_url):
        return jsonify({"error": "URL parameter is invaild"}), 400
    else:
        return jsonify(gettable.main(target_url))

if __name__ == '__main__':
    app.run(debug=True, port=3000)