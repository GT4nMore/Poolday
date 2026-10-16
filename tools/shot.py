"""Headless check of the web build: load, wait, screenshot (and optionally press keys).

    python tools/shot.py NAME [seconds] [url]
"""
import sys
import time

from playwright.sync_api import sync_playwright

name = sys.argv[1]
wait = float(sys.argv[2]) if len(sys.argv) > 2 else 45
url = sys.argv[3] if len(sys.argv) > 3 else 'http://127.0.0.1:8766/index.html?autostart'
CHROME = r'C:/Program Files/Google/Chrome/Application/chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, args=[
        '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
        '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    page = b.new_page(viewport={'width': 1280, 'height': 720})
    logs = []
    page.on('console', lambda m: logs.append(m.text))
    page.goto(url)
    t = time.time()
    shots = 0
    while time.time() - t < wait:
        time.sleep(min(15, wait - (time.time() - t)))
        shots += 1
        page.screenshot(path=f'work/{name}_{shots}.png')
    b.close()
    print('\n'.join(logs[-25:]))
