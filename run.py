#!/usr/bin/env python
from pears import app, db
from pears.models import Profile
import getpass

if __name__ == "__main__":
    user = getpass.getuser()
    profile = Profile(name=user)
    db.session.add(profile)
    db.session.commit()
    app.run(debug=True, host='0.0.0.0')
