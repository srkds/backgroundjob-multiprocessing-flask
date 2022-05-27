
import os
from multiprocessing import Process
import asyncio
from pyppeteer_generation import PdfGeneration

class HandleCpuIntensive:

    def startMultiprocessingTask(self):
        # Running the multiprocess    
        task_cb = Process(target=self.assignPdfGeneration)
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

    def assignPdfGeneration(self):
        # Running async function for pdf generation
        ob = PdfGeneration()

        return asyncio.new_event_loop().run_until_complete(ob.backgroundPdfGeneration())