import webapp2
import jinja2
import os
import random

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

class Question(db.Model):
    """Questions to ask"""
    name = db.StringProperty()
    voteCount = db.IntegerProperty()
    closingDate = db.DateTimeProperty()
    startDate = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):

        questions_options = []
        
        question_query = Question.all()
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
                                   '">' + option.name + '</a> - '
                                   + str(option.voteCount))
            
            questions_options.append((q.name, option_list))
            
        template_values = {
            'questions': questions_options
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
        
        
class Create(webapp2.RequestHandler):
    def post(self):
        
        poll = Question()
        poll.name = self.request.get('question')
        poll.voteCount = 0
        poll.put()
        
        option1 = Option(parent=poll.key())
        option1.name = self.request.get('option1')
        option1.voteCount = 0
        option1.colour = random.randrange(0,255)
        option1.put()
        
        option2 = Option(parent=poll.key())
        option2.name = self.request.get('option2')
        option2.voteCount = 0
        option2.colour = random.randrange(0,255)
        option2.put()
        
        option3 = Option(parent=poll.key())
        option3.name = self.request.get('option3')
        option3.voteCount = 0
        option3.colour = random.randrange(0,255)
        option3.put()
        self.redirect('/')
        
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
        
        """Display a page for that poll?"""
        
        self.redirect('/')
        


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/newpoll', Create),
                               ('/vote/', CastVote)],
                              debug=True)