from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/file")
def getAllTitles():

    f = open("tester.txt", 'r')
    arr = f.readlines()
    f.close()

    for idx in range(len(arr)):
        l, r = arr[idx].split("\t")
        arr[idx] = l

    dict = {"data": arr}

    return json.loads(json.dumps((dict), indent=4))


@ app.route("/file/<id>")
def getSpecificTitle(id):

    f = open("tester.txt", 'r')
    arr = f.readlines()
    f.close()

    def readLine(val):
        line = arr[val]
        l, r = line.split("\t")
        dict = {"data": l}
        return dict

    return json.loads(json.dumps(readLine(int(id)), indent=4))


@ app.route('/file', methods=['POST'])
def appendLabel():
    data = request.json

    title = data["title"]
    keywords = data["keywords"]

    f = open("label.txt", 'a')
    f.write(title + "\t" + '_'.join(k for k in keywords) + "\n")
    f.close()

    return jsonify({"data": "OK"})


@ app.route("/id/latest")
def getLatestIdVal():
    f = open("id.txt", 'r')
    id = f.readline()

    return jsonify({"data": id})


@ app.route("/id/update")
def updateIdVal():
    f = open('id.txt', 'r')
    cur = f.read()
    f.close()
    f = open('id.txt', 'w')
    f.write(str(int(cur)+1))
    f.close()

    # return jsonify({"data": str(int(cur)+1)})
    return jsonify({"data": "Updated"})


if __name__ == "__main__":
    app.run(port=5000)
