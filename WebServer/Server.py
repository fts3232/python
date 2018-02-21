import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'App'))
from App import Application
app = Application()
app.boot()
