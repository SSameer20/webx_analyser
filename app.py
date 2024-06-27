from flask import Flask, request, render_template, jsonify
import tldextract

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            url = data['url']
            url_info = extract_url_info(url)
            return jsonify({"message": "URL processed successfully!", "url_info": url_info})
        else:
            return jsonify({"error": "Unsupported Media Type"}), 415
    return render_template('analyze.html')

def extract_url_info(url):
    extracted = tldextract.extract(url)
    url_info = {
        "subdomain": extracted.subdomain,
        "domain": extracted.domain,
        "suffix": extracted.suffix,
        "registered_domain": extracted.registered_domain
    }
    return url_info

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
