from google.appengine.ext import db


class Opinion(db.Model):
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True, multiline=True)
    vote = db.IntegerProperty(required=True, default=0)
    author = db.StringProperty()
    nickname = db.StringProperty()
    archived = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True)

class Group(db.Model):
    pass
