import sys
import getopt
import re
#import shared
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from shared import *

pool = ConnectionPool('DialectSurvey')
statesFam = ColumnFamily(pool, 'states')
questionsFam = ColumnFamily(pool, 'questions')
choicesFam = ColumnFamily(pool, 'choices')



class State(object):
    def __init__(self,p,n):
        #string
        self.postal=p
        #string
        self.name=n
        #list
        self.questions={}
    def addQuestion(self,q):
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



nameReStr = "<title>Dialect Survey Results: (?P<state>[a-zA-Z ]+) ?</title>"
nameRe = re.compile(nameReStr)

questionReStr = """<table cellpadding="0" cellspacing="0" border="0"><tr><td colspan="4"><b>.*?</table>"""
questionRe = re.compile(questionReStr,re.DOTALL)

questionInfoReStr = """<table cellpadding="0" cellspacing="0" border="0"><tr><td colspan="4"><b>(?P<num>\d{1,3})\. (?P<text>.*?)</b></td></tr>"""
questionInfoRe = re.compile(questionInfoReStr)

choiceReStr = """<tr><td width`"10"></td><td>(?:<b>)? (?P<letter>[a-z])\. (?P<optiontext>.*?) (?:</b>)?</td><td width="20"></td><td>(?:<b>)? \((?P<percentage>(?:[0-9]|\.){1,5}?)%\) (?:</b>)?</td></tr>"""
choiceRe = re.compile(choiceReStr)


#returns a state object from a state html file
def getState(stateFileName, statePostal):
    #if this doesn't work, we have a problem
    f = open(stateFileName)
    stateSource = f.read()
    f.close()
    stateName = nameRe.search(stateSource).groupdict()['state']
    state = State(statePostal, stateName)

    statesFam.insert(statePostal, {'name' : stateName})

    for questionText in questionRe.findall(stateSource):
        info = questionInfoRe.search(questionText).groupdict()
        question = Question(info['num'], info['text'])
        state.addQuestion(question)

        questionsFam.insert(question.number, {'text': info['text']});

        for choiceText in choiceRe.findall(questionText):
            question.add(Choice(*choiceText))
            #print choiceText
            key = statePostal + str(question.number) + choiceText[0]
            choicesFam.insert(key, {'percent' : float(choiceText[2]), 'letter': choiceText[0], 'state': statePostal, 'text': choiceText[1], 'question': question.number})


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
    #statePostal = "OK"
    for statePostal in statePostals:
        state = getState(downloadDirectory + "state_" + statePostal + ".html", statePostal)
        states[statePostal] = state






if __name__ == "__main__":
    sys.exit(main())
