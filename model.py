from google.appengine.ext import db


class Group(db.Model):
    name = db.StringProperty(required=True)
    owner = db.UserProperty(required=True)

class Opinion(db.Model):
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True, multiline=True)
    vote = db.IntegerProperty(required=True, default=0)
    author = db.UserProperty(required=True)
    group = db.ReferenceProperty(Group)
    archived = db.BooleanProperty(default=False)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now_add=True)
