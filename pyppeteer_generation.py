
import os
from pyppeteer import launch
import json
from database_controllers import DatabaseHandle 
from aws_uploads import upload_files


class PdfGeneration:

    async def backgroundPdfGeneration(self):
        print("Inside .............")
        localFileName = "cover1.pdf"
        html_url = "https://google.com"

        # Updating status to inprogress
        db = DatabaseHandle()
        db.updateStatus("InProgress")

        # Pyppeteer pdf generation    
        browser = await launch()
        page = await browser.newPage()
        await page.goto(html_url,timeout=1800000)
        await page.pdf({
            'path': localFileName,
            'margin': { 'bottom': '1.44in', 'top':'0.75in', 'right': '0.52in', 'left':'0.75in' },
            'pageRanges':'1'
        })
        await browser.close()
        print("done")

        # # Storing PDF to AWS S3 bucket
        result = None
        args = {'ACL':'public-read'}
        result = upload_files('./cover1.pdf', '[BUCKET_NAME]', args=args)

        # Updating Status to complete
        db.setUrlAndStatus(result)

        # Deleting Local pdf from server
        if os.path.exists(localFileName):
            os.remove(localFileName)
            print("file deleted from server")
        else:
            print("File not exists")

