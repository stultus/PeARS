#!/usr/bin/env python
from pears import app, db

def create_profile():
    db.create_all()

if __name__ == "__main__":
    create_profile()
    app.run(debug=True, host='0.0.0.0')

