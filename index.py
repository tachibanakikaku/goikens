from google.appengine.api import memcache
from model import Opinion

import webapp2
import cgi, jinja2, logging, os

jinja2_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
  def get(self):
      c = memcache.get('top')
      if c == None:
          q = Opinion.all()
          opinions = q.order('-vote').order('-created')
          template_values = { 'opinions': opinions }
          template = jinja2_environment.get_template('index.html')
          t = template.render(template_values)
          memcache.set('top', t, time=3600)
          self.response.out.write(t)
      else:
          self.response.out.write(c)

class OpinionPage(webapp2.RequestHandler):
  def _put(self):
      if self.request.get('_t') == 'v':
          o = Opinion.get(self.request.get('_k'))
          o.vote += 1
          o.put()

  def post(self):
      if self.request.get('_m') == 'put':
          self._put()
      else:
          o = Opinion(
              title=cgi.escape(self.request.get('title')),
              description=cgi.escape(self.request.get('description')),
              author=cgi.escape(self.request.get('author'))
              )
          o.put()
      memcache.delete('top')
      self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage), ('/opinions', OpinionPage)],
                              debug=True)

