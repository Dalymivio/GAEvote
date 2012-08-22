import webapp2
import jinja2
import os
import random
import imagegen

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import db

class Vote(db.Model):
    """Individual Votes, dated and ID'd as much as poss"""
    date = db.DateTimeProperty(auto_now_add=True)
    
class Option(db.Model):
    """Options to select"""
    name = db.StringProperty()
    voteCount = db.IntegerProperty()
    colour = db.IntegerProperty()
    image = db.BlobProperty()

class Question(db.Model):
    """Questions to ask"""
    name = db.StringProperty()
    voteCount = db.IntegerProperty()
    closingDate = db.DateTimeProperty()
    startDate = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):

        questions_options = []
        
        question_query = Question.all().order('-startDate')
        questions = question_query.fetch(10)
        
        for q in questions:
            option_query = db.GqlQuery("SELECT name, voteCount "
                                  "FROM Option "
                                  "WHERE ANCESTOR IS :1 "
                                  "LIMIT 10",
                                  q.key())
            
            option_query.run()
            option_list = []
            
            for option in option_query:                
                option_list.append('<a href="/vote/?q='
                                   + str(q.key().id()) + 
                                   '&v=' + str(option.key().id()) + 
                                   '">' + option.name + 
                                   ' - <img src="/img/?q='
                                   + str(q.key().id()) +
                                   '&v=' + str(option.key().id())
                                   + '" /></a> - '
                                   + str(option.voteCount))
            
            questions_options.append((q.name, option_list))
            
        template_values = {
            'questions': questions_options
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
        
class CastVote(webapp2.RequestHandler):
    def get(self):
        """pass me the db id of the question then option"""
        q_id = self.request.get('q')
        option_id =  self.request.get('v')
        q = Question.get_by_id(int(q_id))
        option = Option.get_by_id(int(option_id), q)
        
        vote = Vote(parent=option)
        vote.put()
        
        option.voteCount += 1
        option.put()
        
        """Display a page for that poll if from this host, else send back"""
        
        self.redirect('/')
        
class LoadImage(webapp2.RequestHandler):
    def get(self):
        q_id = self.request.get('q')
        option_id =  self.request.get('v')
        q = Question.get_by_id(int(q_id))
        option = Option.get_by_id(int(option_id), q)
        
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(option.image)
        return

class Create(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('new.html')
        self.response.out.write(template.render(template_values))
        
class Create2(webapp2.RequestHandler):
    def post(self):
        
        poll = Question()
        poll.name = self.request.get('question')
        poll.voteCount = 0
        poll.put()        
        
        options = self.request.get_all('option')
        for o in options:
            option = Option(parent=poll.key())
            option.name = o
            option.voteCount = 0
            option.colour = random.randrange(0,255)
            option.image = db.Blob(imagegen.create(option.colour, o)) 
            option.put()
            self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/newpoll', Create2),
                               ('/new', Create),
                               ('/vote/', CastVote),
                               ('/img/', LoadImage)],
                              debug=True)