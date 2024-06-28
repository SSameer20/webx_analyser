from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import socket
import whois
import dns.resolver
import tldextract

app = Flask(__name__)

def get_domain_info(url):
    domain_info = {}
    try:
        # Extract domain
        domain = tldextract.extract(url).registered_domain

        # Get server IP
        domain_info['ip'] = socket.gethostbyname(domain)

        # Get WHOIS information
        whois_info = whois.whois(domain)
        print(whois_info)
        domain_info['location'] = whois_info.get('country')
        domain_info['asn'] = whois_info.get('asn')
        domain_info['isp'] = whois_info.get('isp')
        domain_info['organization'] = whois_info.get('org')
    except Exception as e:
        domain_info['error'] = str(e)
    return domain_info

def get_subdomains(domain):
    subdomains = []
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(f'www.{domain}', 'A')
        for rdata in answers:
            subdomains.append(str(rdata))
    except dns.resolver.NoAnswer:
        pass
    except Exception as e:
        subdomains.append(f'Error: {str(e)}')
    return subdomains

def get_external_resources(url):
    resources = {
        'stylesheets': [],
        'javascripts': [],
        'images': [],
        'iframes': [],
        'anchors': []
    }
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        resources['stylesheets'] = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
        resources['javascripts'] = [script.get('src') for script in soup.find_all('script') if script.get('src')]
        resources['images'] = [img.get('src') for img in soup.find_all('img')]
        resources['iframes'] = [iframe.get('src') for iframe in soup.find_all('iframe')]
        resources['anchors'] = [a.get('href') for a in soup.find_all('a')]
    except Exception as e:
        resources['error'] = str(e)
    return resources

@app.route('/')
def home():
    return render_template('index.html', page="index")

@app.route('/analyse')
def analyze():
    return render_template('analyse.html', page="analyse")

@app.route('/insight')
def insight():
    url = request.args.get('url')
    data = {}
    if url:
        domain = tldextract.extract(url).registered_domain
        data['info'] = get_domain_info(url)
        data['subdomains'] = get_subdomains(domain)
        data['resources'] = get_external_resources(url)
    return render_template('insight.html', data=data, page="insight")

@app.route('/about')
def about():
    return render_template('about.html', page="about")

if __name__ == '__main__':
    app.run(debug=True)
