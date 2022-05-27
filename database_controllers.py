import json

class DatabaseHandle:

    def getStatus(self):
        with open("mock_db.json", "r") as openfile:
            json_obj  = json.load(openfile)

        print(json_obj)
        return json_obj

    def updateStatus(self, status):
        #Updating work status
        dictnary = {
            "status": status,
        }
        json_object = json.dumps(dictnary, indent = 4)
        with open("mock_db.json", "w") as outfile:
            outfile.write(json_object)

    def setUrlAndStatus(self, url):
        # Updating Status to complete
        dictnary = {
            "status": "Completed",
            "url": url
        }
        json_object = json.dumps(dictnary, indent = 4)
        with open("mock_db.json", "w") as outfile:
            outfile.write(json_object)