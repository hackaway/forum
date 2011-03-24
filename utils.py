from mechanize import Browser
import lxml
from lxml import html
import pyodbc
import codecs
#from config import *
import pdb
import re
import urllib2
class NoHistory(object):
  def add(self, *a, **k): pass
  def clear(self): pass
import httplib

exclus = {'%':' percent','&':' and','@':' at ','^':''}

class custom_browser:
    
    def __init__(self):
            self.browser = Browser(history= NoHistory())
            self.browser.set_handle_robots(False) 
            self.browser.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 AskTbPTV/3.8.0.12304 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)')]
            self.loginURL = "http://www.northamericanmotoring.com/forums/members/list/"
            
    def login(self, url , user=None, pwd=None):
        self.browser.open(url) #opens the login url
        #for k in self.browser.forms():
        #    print k
        self.browser.select_form(nr=0) # selects second for which is the login form, first one is the search form
        if user:
            self.browser["vb_login_username"] = user #field named vb_login_username 
        else:
            self.browser["vb_login_username"] = 'somebody'
        if pwd:
            self.browser["vb_login_password"] = pwd #field named vb_login_password
        else:
            self.browser["vb_login_password"] = 'anybody'
        self.browser.submit() #submits the form

class mazda_browser:
    
    def __init__(self):
        self.browser =Browser()
        self.browser.set_handle_robots(False) 
        self.browser.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 AskTbPTV/3.8.0.12304 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)')]

    def login(self, url, user = None, pwd = None):
        self.browser.open(url)
        #for k in self.browser.forms():
        #    print k
        self.browser.select_form(nr=2)
        self.browser["user"] = user 
        self.browser["passwrd"] = pwd
        self.browser.submit()

def xmlTree(url):
    """
        Returnes XML object of a document
        with a given url
    """
    browser = custom_browser()
    
    try:
        response = browser.browser.open(url)
        return html.fromstring(response.read())
    except httplib.BadStatusLine:
        return False
    except urllib2.URLError:
        return False


def xmlTree_w_login(url,ftype, user=None,pwd=None):
    if ftype=='mazda':
            browser = mazda_browser()
    elif ftype=='vb':
        browser = custom_browser()
    else:
        pass
    try:
        browser.login(url,user,pwd)
        response = browser.browser.open(url)
        return html.fromstring(response.read())
    except httplib.BadStatusLine:
        return False
    except urllib2.URLError:
        return False
#audiworld
#bimmerfest
#e90post
#northamericanmotoring
user = 'somebodyis'
pwd = 'anybodyanybody'
fort = 'mazda'
alltime = '&daysprune=-1'
allmosttime = '?daysprune=-1'
sticky = ".//td[contains(@id,'td_threadtitle')]/div/text()"

class Fields:
    def __init__(self, fields, name):
        self.fields = fields
        self.__name__ = name

def addto(ifid,k):
    tmp = int(ifid[1])+40*k
    #print tmp[1]
    retv = ifid[0]+'.'+str(tmp)
    return retv

def diff(s1, s2):
    tmp = re.compile(s1, re.IGNORECASE)
    res = tmp.sub('', s2)
    #print res
    res = res.strip()
    return res

def convert_to_int(s):
    tmp = re.sub(',','',s)
    return tmp

def sanitize(s):
    exc = [r'\xa0']
    for t in exc:
        tmp = re.compile(t, re.UNICODE)
        retv = tmp.sub(' ',s)
    retv = retv.strip()
    return retv

def mysqlfriendly(s):
    for t in exclus.keys():
        s = re.sub(t,exclus[t],s)
    return s


def notvoid(ls):
    if sanitize(ls[1]) != '':
        return True
    else:
        return False
if __name__=='__main__':
    f = u'%^$#@'
    t = mysqlfriendly(f)
    print t
