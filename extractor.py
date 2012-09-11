import sys
import getopt
import re
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

from shared import *

pool = ConnectionPool('DialectSurvey')
states_family = ColumnFamily(pool, 'states')
questions_family = ColumnFamily(pool, 'questions')
choices_family = ColumnFamily(pool, 'choices')



class State(object):
    def __init__(self,p,n):
        #string
        self.postal=p
        #string
        self.name=n
        #list
        self.questions={}
    def add_question(self,q):
        #self.questions.append(q)
        self.questions[q.number] = q




    def __repr__(self):
        return "<S: "+self.postal+">"
class Question(object):
    def __init__(self,n,t):
        #int
        self.number=int(n)
        #string
        self.text=t
        #list
        self.choices=[]
    def add(self, choice):
        self.choices.append(choice)
    def __repr__(self):
        return "<Q: "+self.text+">"
class Choice(object):
    def __init__(self,l,t,p):
        #string
        self.letter=l
        #string
        self.text=t
        #float
        self.percentage=float(p)
    def __repr__(self):
        return "<C: "+self.text+">"

states = {}



name_re_str = "<title>Dialect Survey Results: (?P<state>[a-zA-Z ]+) ?</title>"
name_re = re.compile(name_re_str)

questions_re_str = """<table cellpadding="0" cellspacing="0" border="0"><tr><td colspan="4"><b>.*?</table>"""
question_re = re.compile(questions_re_str,re.DOTALL)

question_info_re_str = """<table cellpadding="0" cellspacing="0" border="0"><tr><td colspan="4"><b>(?P<num>\d{1,3})\. (?P<text>.*?)</b></td></tr>"""
question_info_re_str = re.compile(question_info_re_str)

choice_re_str = """<tr><td width`"10"></td><td>(?:<b>)? (?P<letter>[a-z])\. (?P<optiontext>.*?) (?:</b>)?</td><td width="20"></td><td>(?:<b>)? \((?P<percentage>(?:[0-9]|\.){1,5}?)%\) (?:</b>)?</td></tr>"""
choice_re = re.compile(choice_re_str)


#returns a state object from a state html file
def get_state(state_file_name, state_postal):
    #if this doesn't work, we have a problem
    f = open(state_file_name)
    state_source = f.read()
    f.close()
    state_name = name_re.search(state_source).groupdict()['state']
    state = State(state_postal, state_name)

    states_family.insert(state_postal, {'name' : state_name})

    for question_text in question_re.findall(state_source):
        info = question_info_re_str.search(question_text).groupdict()
        question = Question(info['num'], info['text'])
        state.add_question(question)

        questions_family.insert(question.number, {'text': info['text']});

        for choice_text in choice_re.findall(question_text):
            question.add(Choice(*choice_text))
            #print choice_text
            key = state_postal + str(question.number) + choice_text[0]
            choices_family.insert(key, {'percent' : float(choice_text[2]), 'letter': choice_text[0], 'state': state_postal, 'text': choice_text[1], 'question': question.number})


    return state





















def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
       # process options
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 0;
        # process arguments
        for arg in args:
            process(arg) # process() is defined elsewhere

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    print "starting main"
    #state_postal = "OK"
    for state_postal in state_postals:
        state = get_state(download_directory + "state_" + state_postal + ".html", state_postal)
        states[state_postal] = state




if __name__ == "__main__":
    sys.exit(main())
