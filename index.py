from google.appengine.api import memcache, users
from google.appengine.ext.db import Key

from model import Opinion, Group

import webapp2
import cgi, jinja2, logging, os

jinja2_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      u_link = ('<a href=\"%s\">Sign out</a>' % users.create_logout_url('/'))
      c = memcache.get('top')
      if c == None:
        opinions = Opinion.gql("WHERE archived = :1 ORDER BY vote DESC, created DESC", False)
        template_values = { 'opinions' : opinions, 'u_link' : u_link }
        template = jinja2_environment.get_template('html/index.html')
        t = template.render(template_values)
        memcache.set('top', t, time=3600)
        self.response.out.write(t)
      else:
        self.response.out.write(c)
    else:
      u_link = ('<a href=\"%s\">sign in</a>' % users.create_login_url('/'))
      self.response.out.write('<html><body>%s</body></html>' % u_link)

class OpinionPage(webapp2.RequestHandler):
  def get(self):
    g = Group.get(self.request.get('g'))
    opinions = Opinion.gql("WHERE group = :1", g)
    template_values = { 'opinions' : opinions, 'g' : g }
    template = jinja2_environment.get_template('html/opinion.html')
    t = template.render(template_values)
    self.response.out.write(t)

  def _put(self):
    o = Opinion.get(self.request.get('_k'))
    if self.request.get('_t') == 'v':
      o.vote += 1
      o.put()
    elif self.request.get('_t') == 'f':
      o.archived = True
      o.put()

  def _delete(self):
    if self.request.get('_t') == 'd':
      o = Opinion.get(self.request.get('_k'))
      o.delete()

  def post(self):
    print 'aaaaaaaa'
    if self.request.get('_m') == 'put':
      self._put()
    elif self.request.get('_m') == 'delete':
      self._delete()
    else:
      o = Opinion(
        title = cgi.escape(self.request.get('title')),
        description = cgi.escape(self.request.get('description')),
        author = users.get_current_user(),
        group = Key(self.request.get('g'))
        )
      o.put()
    memcache.delete('top')
    self.redirect('/')

class GroupPage(webapp2.RequestHandler):
  def get(self):
    template = jinja2_environment.get_template('html/group.html')
    gs = Group.all()
    template_values = { 'groups' : gs }
    t = template.render(template_values)
    self.response.out.write(t)
    
  def post(self):
    g = Group(
      name=cgi.escape(self.request.get('name')),
      owner=users.get_current_user()
      )
    g.put()
    self.redirect('/groups')
    
class TaskPage(webapp2.RequestHandler):
  def get(self):
    if (self.request.get('t') == 'update_schema'):
      opinions = Opinion.all()
      for o in opinions:
        o.put()

app = webapp2.WSGIApplication([('/', MainPage), ('/opinions', OpinionPage), ('/groups', GroupPage), ('/tasks', TaskPage)],
                              debug=True)

