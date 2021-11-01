import json

from flask import Flask, render_template, request, Response
from werkzeug.wsgi import FileWrapper

from genDoc import genDoc

app = Flask(__name__)

branches={}

with open('branches.json') as reader:
    branches=json.load(reader)


@app.route('/')
def base():
    companies=[]
    for reg in range(1,5):
        for comp in list('ABCDEFGHI'):
            companies.append(f"{comp}{reg}")
    return render_template('base.html',branches=branches,companies=companies)

@app.route('/genDoc')
def generateDoc():
    if request.method=='GET':
        file=genDoc.generateMFR()
        file=FileWrapper(file)
        return Response(file, mimetype="doc.pdf", direct_passthrough=True)




if __name__ == '__main__':
    app.run()
