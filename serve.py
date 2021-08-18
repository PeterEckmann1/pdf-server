import re
from collections import Counter
from flask import Flask, request
from secrets import token_hex
import subprocess
import os


app = Flask(__name__, static_url_path='', static_folder='pdfs')


@app.route('/', methods=['POST'])
def upload():
    token = token_hex(20)
    file = request.files['file']
    file.save(f'pdfs/{token}.pdf')
    os.mkdir(f'pdfs/{token}')
    filename = f"{file.filename.replace('.pdf', '')}.html"
    subprocess.call(['pdftohtml', '-c', '-s', f'../{token}.pdf', filename], cwd=f'pdfs/{token}')
    filename = filename.replace('.html', '-html.html')
    f = open(f'pdfs/{token}/{filename}', 'r+', encoding='utf-8')
    html = f.read()
    dois = re.findall('10\\.[0-9]{4,9}/[-._;()/:a-zA-Z0-9]+', html)
    if dois:
        doi = Counter(dois).most_common(1)[0][0]
        html = html.replace('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>',
                            f'<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta name="DC.Identifier" content="{doi}"/>')
    pages = []
    for page in html.split('<!DOCTYPE html>'):
        for css_class in re.findall('\\.ft[0-9]+{', page):
            new_css = 'a' + token_hex(20)
            page = page.replace(css_class, f'.{new_css}{{')
            page = page.replace(css_class.replace('.', 'class="').replace('{', '"'), f'class="{new_css}"')
        pages.append(page)
    f.seek(0)
    f.write('<!DOCTYPE html>'.join(pages))
    f.truncate()

    return {'loc': f'/{token}/{filename}'}


if __name__ == '__main__':
    app.run()