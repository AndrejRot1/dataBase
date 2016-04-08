import os
import cgi
import urllib
from webapp2_extras import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2


views_dir = os.path.join(os.path.dirname(__file__), 'views')

class Message(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
  
    name = ndb.StringProperty(indexed = True)
    surname = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    subject = ndb.StringProperty(indexed=False)
    message = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class Account(ndb.Model):
  username = ndb.StringProperty()
  userid = ndb.IntegerProperty()
  email = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)



class Handler(webapp2.RequestHandler):
  def render(self, filename):
    f = open(views_dir + '/' + filename)
    self.response.write(f.read())
    f.close()

class Index(Handler):
  def get(self):
    self.render('index.html')

class Post(Handler):


  def get(self):
    self.render('post.html')
    
  def post(self):
    self.render('post.html')
    
    form_input = Message(name = self.request.get('field1'),
			 surname = self.request.get('field2'),
                         email = self.request.get('field3'),
                         subject = self.request.get('field4'),
                         message = self.request.get('field5'))

  
    form_input_key = form_input.put()  

    
class Retrive(Handler,Account):

  def _render(self,template,**value):
    j = jinja2.get_jinja2()
    html = j.render_template(template,**value)
    self.response.write(html) 

  def get(self):
    messg = Message.query().fetch(100)
    self._render('retrive.html',messg = messg)
   
         
        
app = webapp2.WSGIApplication([
    ('/', Index),
    ('/post',Post),
    ('/retrive',Retrive),
], debug=True)
