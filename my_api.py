from flask import Flask, request
from waitress import serve
from flask_cors import CORS
from multiprocessing import Process
import asyncio
from pyppeteer import launch
from PyPDF2 import PdfFileMerger
import json
from aws_uploads import upload_files
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*":{"origin":"*"}})


@app.route("/api/jobstatus",methods=['GET'])
def getBackgroundJobStatus():
    """ 
    - Use this route to get status of the background work
    - client will periodicaly call this endpoint ex. after every 1 or 2 seconds
    """
    with open("mock_db.json", "r") as openfile:
        json_obj  = json.load(openfile)

    print(json_obj)
    return json_obj


@app.route("/api/generate/pdf", methods=['POST'])
def handleGeneratePdfRequest():
    html_url = request.json.get("html_url")
    body_operator = request.json.get('operator')
    if html_url is None or body_operator is None:
        return "Bad request, invalid job id: %s or operator: %s" % (1,body_operator), 401
    
    #Updating work status
    dictnary = {
        "status": "Not Yet Started",
    }
    json_object = json.dumps(dictnary, indent = 4)
    with open("mock_db.json", "w") as outfile:
        outfile.write(json_object)

    # Running the multiprocess    
    task_cb = Process(target=assignPdfGeneration)
    task_cb.start()

    # Setting CPU affiniity
    print(task_cb.pid)
    pid1 = task_cb.pid
    affinity = os.sched_getaffinity(pid1)
    print("Process is eligible to run on:", affinity)
    affinity_mask = {
            0
        }
    os.sched_setaffinity(pid1, affinity_mask)
    print("CPU affinity mask is modified for process id % s" % pid1)
    affinity = os.sched_getaffinity(pid1)
    # Print the result
    print("Now, process is eligible to run on:", affinity)

    return "Job is received ", 202

def assignPdfGeneration():
    # Running async function for pdf generation
    return asyncio.new_event_loop().run_until_complete(backgroundPdfGeneration())

async def backgroundPdfGeneration():
    print("Inside .............")

    # Updating status to inprogress
    dictnary = {
        "status": "InProgress",
    }
    json_object = json.dumps(dictnary, indent = 4)
    with open("mock_db.json", "w") as outfile:
        outfile.write(json_object)

    # Pyppeteer pdf generation    
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://google.com',timeout=1800000)
    await page.pdf({
        'path': 'cover1.pdf',
        'margin': { 'bottom': '1.44in', 'top':'0.75in', 'right': '0.52in', 'left':'0.75in' },
        'pageRanges':'1'
    })
    await browser.close()
    print("done")

    # Storing PDF to AWS S3 bucket
    result = None
    args = {'ACL':'public-read'}
    result = upload_files('./cover1.pdf', 'BUCKET_NAME', args=args)

    # Updating Status to complete
    dictnary = {
        "status": "Completed",
        "url": result
    }
    json_object = json.dumps(dictnary, indent = 4)
    with open("mock_db.json", "w") as outfile:
        outfile.write(json_object)

    # Deleting Local pdf from server
    if os.path.exists("cover1.pdf"):
        os.remove("cover1.pdf")
        print("file deleted from server")
    else:
        print("File not exists")

    print(page)
    return page

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=6060)


"""
To see (process)pid's affinity

$> taskset -c -p <pid>

to view task manager type
$> top 

"""
