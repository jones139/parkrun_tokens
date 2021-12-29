import os
import flask
import finish_tokens
import json
import werkzeug

app = flask.Flask(__name__)
tmpFilesLst = []

def deleteTmpFiles():
    global tmpFilesLst
    #if not 'tmpFilesLst' in locals():
    #    print("deleteTmpFiles - Creating tmpFilesLst")
    #    tmpFilesLst = []
    print("deleteTmpFiles(): tmpFilesLst=",tmpFilesLst)
    for fname in tmpFilesLst:
        if (os.path.exists(fname)):
            print("Deleting Temporary File: %s" % fname)
            os.remove(fname)
        else:
            print("temporary file %s does not exist - ignoring" % fname)
    tmpFilesLst = []

@app.route("/")
def hello():
    #return "Hello World from parkrun tokens web app"
    return flask.redirect("/static/index.html", code=302)

@app.route("/finish-tokens", methods=['GET', 'POST'])
def finishTokens():
    print(flask.request.values)
    deleteTmpFiles()
    prNameTxt = flask.request.values.get('pRunName')
    tokensTxt = flask.request.values.get('tokensTxt')
    dataTxt = flask.request.data.decode("utf-8")
    print("prNameTxt=",prNameTxt)
    print("tokensTxt=",tokensTxt)
    tokenLst = finish_tokens.makeTokenList(tokensTxt)
    zipBytesIO = finish_tokens.getTokensZipFile(tokenLst,prNameTxt)
    #tmpFilesLst.append(zipFname)
    #print("tmpFilesLst=",tmpFilesLst)
    return(flask.send_file(zipBytesIO, attachment_filename="tokens.zip", as_attachment=True))


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
