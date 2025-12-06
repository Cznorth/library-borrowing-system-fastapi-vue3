import os
import glob
import subprocess
from pathlib import Path

BASE = Path(__file__).parent
EXPORT = BASE / 'exports'
EXPORT.mkdir(exist_ok=True)

FORMAT = os.environ.get('UML_FORMAT', 'png')  # png or jpg
PLANTUML_JAR = os.environ.get('PLANTUML_JAR', str(BASE.parent / 'tools' / 'plantuml.jar'))

def render_with_jar(puml_path: Path):
    dot = r"C:\Program Files\Graphviz\bin\dot.exe"
    cmd = [
        'java', '-jar', PLANTUML_JAR,
        f'-t{FORMAT}', '-o', str(EXPORT)
    ]
    if os.path.exists(dot):
        cmd.extend(['-graphvizdot', dot])
    cmd.append(str(puml_path))
    subprocess.check_call(cmd, cwd=str(BASE))

def convert_png_to_jpg():
    if FORMAT.lower() != 'jpg':
        return
    try:
        from PIL import Image  # type: ignore
    except Exception:
        return
    for png in EXPORT.glob('*.png'):
        img = Image.open(png).convert('RGB')
        jpg = png.with_suffix('.jpg')
        img.save(jpg, quality=90)

def main():
    for p in glob.glob(str(BASE / '*.puml')):
        render_with_jar(Path(p))
    convert_png_to_jpg()

if __name__ == '__main__':
    main()

