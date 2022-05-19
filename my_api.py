from flask import Flask, request
from waitress import serve
from flask_cors import CORS
from multiprocessing import Process
import asyncio
from pyppeteer import launch
from PyPDF2 import PdfFileMerger
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*":{"origin":"*"}})

@app.route("/",methods=['GET'])
def helloWorld():
    """ 
    Use this route to get status of the background work
    """
    with open("mock_db.json", "r") as openfile:
        json_obj  = json.load(openfile)

    print(json_obj)
    return json_obj

@app.route("/task/<job_id>",methods=['POST'])
def task(job_id):
    body_job_id = request.json.get("job_id")
    body_operator = request.json.get('operator')
    if body_job_id is None or body_operator is None:
        return "Bad request, invalid job id: %s or operator: %s" % (body_job_id,body_operator), 401
    # output=run_task(body_job_id,body_operator)
    # return output,201
    # task_cb = Process(target=run_task, args=(body_job_id,body_operator))
    # va1 = 10


    """ Updating work status """

    dictnary = {
        "status": "Not Yet Started",
    }

    json_object = json.dumps(dictnary, indent = 4)

    with open("mock_db.json", "w") as outfile:
        outfile.write(json_object)

    task_cb = Process(target=test)
    # task_cb2 = Process(target=test)
    task_cb.start()
    # task_cb2.start()
    return "Job id %s received " % job_id, 202

def test():
    print("Done.......")
    asyncio.new_event_loop().run_until_complete(run_task())
    # return "Job id Done " , 202

async def run_task():
    print("Inside .............")

    """ Updating status to inprogress """

    dictnary = {
        "status": "InProgress",
    }

    json_object = json.dumps(dictnary, indent = 4)

    with open("mock_db.json", "w") as outfile:
        outfile.write(json_object)

    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://google.com',timeout=1800000)
    await page.pdf({
        'path': 'cover1.pdf',
        'margin': { 'bottom': '1.44in', 'top':'0.75in', 'right': '0.52in', 'left':'0.75in' },
        'pageRanges':'1'
    })

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

    """ Updating Status to complete """

    dictnary = {
        "status": "Completed"
    }

    json_object = json.dumps(dictnary, indent = 4)

    with open("mock_db.json", "w") as outfile:
        outfile.write(json_object)

    print("done")
    return "done", 202

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=6060)
    # serve(app, port=6060)