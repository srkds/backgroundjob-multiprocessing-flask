from flask import Flask, request
from flask_cors import CORS
from aws_uploads import upload_files
from pyppeteer_generation import PdfGeneration
from database_controllers import DatabaseHandle 
from controllers import HandleCpuIntensive 

app = Flask(__name__)
cors = CORS(app, resources={r"/*":{"origin":"*"}})


@app.route("/api/jobstatus",methods=['GET'])
def getBackgroundJobStatus():
    """ 
    - Use this route to get status of the background work
    - client will periodicaly call this endpoint ex. after every 1 or 2 seconds
    """
    db = DatabaseHandle()
    json_obj = db.getStatus()
    return json_obj


@app.route("/api/generate/pdf", methods=['POST'])
def handleGeneratePdfRequest():
    html_url = request.json.get("html_url")
    body_operator = request.json.get('operator')
    if html_url is None or body_operator is None:
        return "Bad request, invalid job id: %s or operator: %s" % (1,body_operator), 401
    
    #Updating work status

    db = DatabaseHandle()
    db.updateStatus("Not Yet Started")
    
    mp = HandleCpuIntensive()
    mp.startMultiprocessingTask()
    
    return "Job is received ", 202


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=6060)


"""
To see (process)pid's affinity

$> taskset -c -p <pid>

to view task manager type
$> top 

"""
