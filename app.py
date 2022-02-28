from mimetypes import MimeTypes
from typing import List, Dict, Any
from pathlib import Path
from re import TEMPLATE
from tempfile import TemporaryDirectory
import jinja2
import time
import subprocess

from flask import Flask, make_response, request, abort, send_file

TEMPLATEX_PATH = Path('./templatex/')
XELATEX_BIN = '/usr/bin/xelatex'

def getJinjaEnv(loaderPath=Path('.')):
    return jinja2.Environment(
        block_start_string='\\BLOCK{',
        block_end_string='}',
        variable_start_string='\\VAR{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(loaderPath)
    )

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    env = getJinjaEnv(TEMPLATEX_PATH)

    def gen_latex(tpath: Path, data: List[Dict[str, Any]]) -> str:
        template = env.get_template(str(tpath))
        return template.render(data)

    @app.route('/pdf/<string:tname>', methods=['POST'])
    def pdf(tname: str): 
        if not tname.endswith('.tex'):
            tname += '.tex'

        try:
            with TemporaryDirectory(prefix='cttex_') as d:
                tpath = Path(d) / tname
                with open(tpath, 'w') as f:
                    f.write(gen_latex(tname, request.json))
                
                out = subprocess.check_call([XELATEX_BIN, '-interaction=batchmode', tname], cwd=d)
                out = subprocess.check_call([XELATEX_BIN, '-interaction=batchmode', tname], cwd=d)

                return send_file(tpath.with_suffix('.pdf'))
        except jinja2.exceptions.TemplateNotFound:
            abort(404)

    @app.route('/tex/<string:tname>', methods=['POST'])
    def tex(tname: str):
        if not tname.endswith('.tex'):
            tname += '.tex'

        try:
            response = make_response(gen_latex(tname, request.json))
            response.mimetype = 'text/plain'
            return response
        except jinja2.exceptions.TemplateNotFound:
            abort(404)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
