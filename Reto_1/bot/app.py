from selenium import webdriver
import requests
import sys
import os
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, flash, request

app = Flask(__name__)

def visitar(sitio_a_visitar):
    session = requests.Session()

    r = session.get("http://127.0.0.1:5000/login")
    soup = BeautifulSoup(r.text, 'html.parser')

    csrf_token = None
    csrf_element = soup.find('input', {'name': 'csrf_token'})
    csrf_token = csrf_element['value']

    login_data = {
        "username": "admin",
        "password": os.getenv('ADMIN_PASSWORD'),
        "csrf_token": csrf_token,
        "submit": "Login"
    }

    r = session.post("http://127.0.0.1:5000/login", data=login_data)

    for cookie in session.cookies:
        cookie_val = cookie.value

    #cookie = r.headers['Set-Cookie'].split("=")[1]

    print(cookie_val)

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Ejecutar en modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Firefox(options=options, service_log_path='/dev/null')

    browser.get('http://127.0.0.1:5000/')

    browser.add_cookie({'name': 'session', 'value': cookie_val})

    browser.get("http://127.0.0.1:5000"+sitio_a_visitar)

    browser.quit()

@app.route('/visit_post')
def index():
    
    query = request.args.get('query')

    visitar(query)

    return "send from admin!"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=7000)
