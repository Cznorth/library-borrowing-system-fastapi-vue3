import os
import glob
import requests
import zlib

BASE = os.path.dirname(__file__)
EXPORT = os.path.join(BASE, 'exports')
os.makedirs(EXPORT, exist_ok=True)

FORMAT = os.environ.get('UML_FORMAT', 'svg')
KROKI = os.environ.get('KROKI_URL', f'https://kroki.io/plantuml/{FORMAT}')
KROKI_RENDER = os.environ.get('KROKI_RENDER', 'https://kroki.io/render')
PUML = os.environ.get('PUML_URL', f'http://www.plantuml.com/plantuml/{FORMAT}/')

def _encode64(data: bytes) -> str:
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_' 
    res = []
    for i in range(0, len(data), 3):
        b = data[i:i+3]
        while len(b) < 3:
            b += b'\x00'
        b1, b2, b3 = b[0], b[1], b[2]
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        res.append(alphabet[c1] + alphabet[c2] + alphabet[c3] + alphabet[c4])
    return ''.join(res)

def _plantuml_encode(text: str) -> str:
    c = zlib.compress(text.encode('utf-8'))
    d = c[2:-4]
    return _encode64(d)

def render_file(path: str):
    with open(path, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8')
    r = requests.post(KROKI_RENDER, json={'diagram_type': 'plantuml', 'diagram_source': text, 'output_format': FORMAT})
    if r.status_code >= 400:
        r = requests.post(KROKI, data=text.encode('utf-8'), headers={'Content-Type': 'text/plain'})
    if r.status_code >= 400:
        code = _plantuml_encode(text)
        r = requests.get(PUML + code)
    if r.status_code >= 400:
        print('failed', path, r.status_code)
        return
    name = os.path.splitext(os.path.basename(path))[0] + f'.{FORMAT}'
    out = os.path.join(EXPORT, name)
    with open(out, 'wb') as f:
        f.write(r.content)
    print('generated', out)

def main():
    for p in glob.glob(os.path.join(BASE, '*.puml')):
        render_file(p)

if __name__ == '__main__':
    main()

