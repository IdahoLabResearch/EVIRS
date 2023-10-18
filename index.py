# for HTTP requesthanders ( to map the request to request handlers)
from pathlib import Path
import tornado.web

# imprting the main event loop
import tornado.ioloop

import os
import numpy as np
import pandas as pd
import handlers

# 5YJ3GDEF2LFR00942, 220, 330, 322
# JN1AZ0CP7CT024420 (Nissan)
# 5YJ3GDEF2LFR00942

# 5YJYGDEE3MF071288 Tesla, 2020, Model Y
# 5YJYGDEF2LFR00942 Tesla, 2021, Model X
# (Carmax) 5YJ3E1EA2KF308202 Tesla, 2019, Model 3, Standard Range
# (Carmax) 5YJYGDEF8MF216589 Tesla, 2021, Model Y, Performance 
# (Carmax) 5YJYGDEE8MF131517 Tesla, 2021, Model Y, Long Range 
# (Carmax) 5YJXCDE22KF184398 Tesla, 2019, Model X, Standard Range 
# KM8K3CAB9NU876739 kona

# 5YJ3F7EA_LF4nnnnn

class Application(tornado.web.Application):
    def __init__(self):
        apphandlers = [
            (r"/", handlers.mainRequestHandler),
            (r"(/check_vin)$", handlers.getSubmodelsByVINHandler),
            (r"(/get_makes)", handlers.getMakesHandler),
            (r"(/get_models)", handlers.getModelsHandler),
            (r"(/get_years)", handlers.getYearsHandler),
            (r"(/get_submodels)", handlers.getSubmodelsHandler),
            (r"(/validate_form)", handlers.validateFormHandler)
        ]
        settings = {
            # "debug": True,
            # "template_path": os.path.join(config.base_dir, "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static") # folder for css, js, etc, files
        }
        tornado.web.Application.__init__(self, apphandlers, **settings)

if __name__ == "__main__":
    app = Application()
    port = 8882
    app.listen(port)
    print(f"Web service is ready and listening on port {port}")

    # start the server on the current thread
    tornado.ioloop.IOLoop.current().start()

