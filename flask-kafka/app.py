import sys
from flask import Flask
from pathlib import Path

from api.bootstrap import Bootstrap
from api.controller.consumer_controller import consumer
from api.controller.producer_controller import producer
"""
Author : Neda Peyrone
Create Date : 30-08-2023
File : app.py
"""
def create_app():
  path = Path().absolute()
  Bootstrap(path) # load parameters from the YAML file

  app = Flask(__name__)
  app.register_blueprint(consumer)
  app.register_blueprint(producer)
  return app

if __name__ == '__main__':
  try:
    port = int(sys.argv[1])
  except Exception:
    port = 8081
    
  create_app().run(host='0.0.0.0', port=port, debug=True, use_reloader=True)
