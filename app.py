import json

from flask import Flask, render_template, request, Response
from werkzeug.wsgi import FileWrapper

from genDoc import genDoc

app = Flask(__name__)

branches={}

with open('/home/branching/branches.json') as reader:
    branches=json.load(reader)


@app.route('/')
def base():
    companies=[]
    for reg in range(1,5):
        for comp in list('ABCDEFGHI'):
            companies.append(f"{comp}{reg}")
    return render_template('base.html',branches=branches,companies=companies)

@app.route('/genDoc', methods=['POST'])
def generateDoc():
    file=genDoc.generateMFR(
        request.values.get("company")[0],
        request.values.get("company")[1],
        request.values.get("first"),
        request.values.get("last"),
        request.values.get("email"),
        request.values.get("prefs")
    )
    file=FileWrapper(file)
    return Response(file, mimetype="doc.pdf", direct_passthrough=True)




if __name__ == '__main__':
    app.run()
