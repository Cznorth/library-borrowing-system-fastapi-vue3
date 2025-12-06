import os
import glob
import requests

BASE = os.path.dirname(__file__)
EXPORT = os.path.join(BASE, 'exports')
os.makedirs(EXPORT, exist_ok=True)

SERVER = 'http://www.plantuml.com/plantuml/png'

def render_file(path: str):
    with open(path, 'rb') as f:
        data = f.read()
    r = requests.post(SERVER, data=data)
    name = os.path.splitext(os.path.basename(path))[0] + '.png'
    out = os.path.join(EXPORT, name)
    with open(out, 'wb') as f:
        f.write(r.content)
    print('generated', out)

def main():
    for p in glob.glob(os.path.join(BASE, '*.puml')):
        render_file(p)

if __name__ == '__main__':
    main()

