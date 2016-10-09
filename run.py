#!/usr/bin/env python
from pears import app, db
from pears.models import Profile
import getpass

@app.before_first_request
def create_profile():
    db.create_all()
    user = getpass.getuser()
    profiles = Profile.query.all()
    if not profiles:
        profile = Profile(name=user)
        db.session.add(profile)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

