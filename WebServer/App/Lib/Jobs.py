import os
import threading
import subprocess


class Jobs:
    '定时任务类'

    def run(self):
        root = os.path.join(os.getcwd(), 'App/Jobs')
        for x in os.listdir(root):
            task = threading.Thread(target=self.job, args=(root, x))
            task.setDaemon(True)
            task.start()

    def job(self, root, filename):
        subprocess.Popen(["python", filename], shell=True, stdout=subprocess.PIPE, cwd=root)
