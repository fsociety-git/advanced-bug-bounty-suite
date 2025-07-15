import json
from jinja2 import Environment, FileSystemLoader
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def take_screenshot(url, output_path):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1920, 1080)
        driver.get(url)
        time.sleep(2)
        driver.save_screenshot(output_path)
        driver.quit()
        return output_path
    except Exception as e:
        print(f"Screenshot error for {url}: {e}")
        return None

def generate_report(findings, formats=['json']):
    os.makedirs('reports', exist_ok=True)
    for i, f in enumerate(findings):
        if 'url' in f:
            shot_path = f"reports/screenshot_{i}.png"
            captured = take_screenshot(f['url'], shot_path)
            if captured:
                f['screenshot'] = shot_path
    if 'json' in formats:
        with open("reports/report.json", "w") as f:
            json.dump(findings, f, indent=4)
    if 'html' in formats:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report.html.jinja')
        html = template.render(findings=findings)
        with open("reports/report.html", "w") as f:
            f.write(html)
    if 'pdf' in formats:
        c = canvas.Canvas("reports/report.pdf")
        y = 800
        for f in findings:
            c.drawString(100, y, str(f))
            if 'screenshot' in f:
                c.drawImage(f['screenshot'], 100, y-200, width=400, preserveAspectRatio=True)
            y -= 300
        c.save()
    print("Reports generated in reports/.")
