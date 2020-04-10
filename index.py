import spacy, os, atexit, random, pymongo
from flask import  Flask, jsonify, request
from spacy.gold import GoldParse
from spacy.language import EntityRecognizer

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["train"]
mycol = mydb["snippet"]

app = Flask(__name__)

cron = Scheduler(daemon=True)
cron.start()

@cron.interval_schedule(hours=1)
def job_function():
    request = {"trained": False}
    results = mycol.find(request)
    
    

@app.route('/', methods=['GET'])
def get_training_directories():
    if request.method == 'GET':
        directories = os.listdir('.')
        return jsonify({"data": directories})

@app.route('/', methods=['POST'])
def make_training_directoreis():
    body = request.get_json(force=True)
    try:
        path = f'./{body['name']}'
        os.mkdir(path)
    except OSError:
        return jsonify({"error": "Creation of the directory %s failed" % path},code=[400])
    else:
        return jsonify({"message": "success"},code=[201])
        
@app.route('/', methods=['PUT']) 
def amend_existing_model(): 
    body  = request.get_json(force=True)
    thedict = { "name": body['name'], "label": body['label'], "sentence": body['sentence'], "training_data": body['training_data'], "trained": False }
    doc = mycol.insert_one(thedict)
    return jsonify({ "doc": doc.inserted_id })


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')