from selenium import webdriver
import requests
from bs4 import BeautifulSoup

def visitar(sitio_a_visitar):
    session = requests.Session()

    r = session.get("http://127.0.0.1:5000/login")
    soup = BeautifulSoup(r.text, 'html.parser')

    csrf_token = None
    csrf_element = soup.find('input', {'name': 'csrf_token'})
    csrf_token = csrf_element['value']

    login_data = {
        "username": "admin",
        "password": "password123",
        "csrf_token": csrf_token,
        "submit": "Login"
    }

    r = session.post("http://127.0.0.1:5000/login", data=login_data)

    for cookie in session.cookies:
        cookie_val = cookie.value

    #cookie = r.headers['Set-Cookie'].split("=")[1]

    print(cookie_val)

    browser = webdriver.Firefox()

    browser.get('http://127.0.0.1:5000/')

    browser.add_cookie({'name': 'session', 'value': cookie_val})

    browser.get("http://127.0.0.1:5000"+sitio_a_visitar)

    browser.quit()

visitar("/post/4")

