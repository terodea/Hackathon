"""Routes for the course resource.
"""

"""
-------------------------------------------------------------------------
Challenge general notes:
-------------------------------------------------------------------------

1. Bonus points for returning sensible HTTP codes from the API routes
2. Bonus points for efficient code (e.g. title search)
"""
from configs.log import loggerClass
from flask import Flask
import data
lg  = loggerClass("courses")
app = Flask(__name__)

# Import the API routes
from routes.course import *

# Required because app is imported in other modules
if __name__== '__main__':
    print("Loading data", end=" ")
    data.load_data()
    print("... done")
    app.run(debug=True)
