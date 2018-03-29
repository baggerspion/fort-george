#!/usr/bin/env python3

import sync

from flask import Flask

app = Flask(__name__)
@app.route("/sync")
def do_sync():
    sync.complete_sync()    
    return 'Sync completed' 

if __name__ == '__main__':
    app.run()
