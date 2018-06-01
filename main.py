import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Post(db.Model):
    title = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        t = jinja_env.get_template('index.html')
        self.response.out.write(t.render( posts= posts ))

class NewPost(webapp2.RequestHandler):
    def get(self, error=""):
        t = jinja_env.get_template('new-post.html')
        self.response.out.write(t.render(error=error))

    def post(self):
        title = self.request.get('title')
        text = self.request.get('content')
        if title and text:
            new_post = Post(title=title, text=text)
            new_post.put()
        else:
            self.get(error="You have to put something in the both filds.")
app = webapp2.WSGIApplication([('/', MainPage), ('/new-post', NewPost)])
