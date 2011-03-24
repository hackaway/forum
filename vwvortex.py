import re
from datetime import date, timedelta
import time
from utils import *
VWVORTEX = 'http://forums.vwvortex.com/'#forum.php'

class vwvortex:
    
    def __init__(self):
        self.domain = VWVORTEX
        self.main_cat = "(//ul/li[contains(@class,'navbit')][last()-1])[1]"
        self.cur_cat = "(//ul/li[contains(@class,'navbit')][last()])[1]"
        self.linklist_lvl1 = "//span[@class='forumtitle']/a/@href"
        self.linklist_lvl2 = "//h2[@class='forumtitle']/a/@href"
        self.threads_list = "//a[contains(@id,'thread_title')]/@href"
        self.next_link = "(//a[contains(@title,'Next Page')]/@href)[1]"

        self.member_list_url ="http://forums.vwvortex.com/member.php?%s"
        
        self.threaddata = "//div/ol[@id='threads']/li/div"
        self.description = ".//a[starts-with(@id,'thread_title')]"
        #self.views = ".//td[starts-with(@class,'stats')]"
        self.replies = ".//li[contains(.,'Replies')]/a"
        self.views = ".//li[contains(.,'Views')]"
        self.link = "..//a[starts-with(@id,'thread_title')]/@href"


        self.postdata = "//ol[@id='posts']/li[starts-with(@id,'post_')]"
        self.timeofpost =".//span[@class='date']"  #this needs to be parsed further in order to extract the time of the post
        self.posterid = ".//a[starts-with(@class,'username')]/@href" #needs to be parsed to get the poster id
        self.postid = ".//a[@class='postcounter']/@href" #needs to be parsed to get the post id
        self.postcount =".//a[@class='postcounter']" #needs some programming
        self.postlink = ".//a[@class='postcounter']/@href"
        
        self.lastac = "//dl[@class='stats']/dt[contains(.,'Last Activity')]/following-sibling::*[1]"
        self.joindate = "//dl[@class='stats']/dt[contains(.,'Join Date')]/following-sibling::*[1]"
        self.handle = "//span[@id='userinfo']/text()"
        self.location = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Location')]/following-sibling::*"
        self.name = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Name')]/following-sibling::*"
        self.interests = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Interests')]/following-sibling::*"
        self.occupation = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Occupation')]/following-sibling::*"
        self.cars = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Year/Make')]/following-sibling::*"
        self.ulink = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'This Page')]/following-sibling::*"
        self.noposts = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Total Posts')]/following-sibling::*"
        self.ppday = "//div[@id='view-aboutme']//dl[@class='stats']//dt[contains(.,'Posts Per Day')]/following-sibling::*"

    def parse_views(self, tmp):
        #tmpv =  
        views = {}
        views['Views'] = tmp.split(' ')[1].strip()
        return views
	

    def thread_id(self, tmp):
        return tmp.split('?')[1].split('-')[0]

    def post_id(self, tmp):
         #print tmp       
        return tmp.split('#post')[1]
                
    def poster_id(self, tmp):
         #print tmp      
        return tmp.split('php?')[1].split('-')[0]

    def join_date(self, tmp):
        return tmp.strip()

    def total_posts(self, tmp):
        tmp.strip()
        tmp = convert_to_int(tmp)
        return tmp
    def last_activity(self, tmp):
            #tmp = re.sub(u'\\xa',' ',tmp)
            tmp = tmp.strip()
            #print tmp
            tmp = sanitize(tmp)
            v1 = r'[yester|to]+day[\s|\\xa0]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            v2 = r'[yester|to]+day[\s|\\xa|\,\s|\s\,]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            d1 = r'[\d]{2}-[\d]{2}-[\d]{4}[\s|\,\s|\\xa0]{1}[\d]{2}:[\d]{2}'
            d3 = r'[\d]{2}-[\d]{2}-[\d]{4}[\s|\,\s|\\xa0]{1,2}[\d]{2}:[\d]{2}[\s]+[AM|PM]+'
            d2 = r'[yester|to]+day[\s]+at[\s]{1}[\d]{2}[:][\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            if re.search(v1, tmp, re.IGNORECASE):
                
                actual = re.search(v1, tmp, re.IGNORECASE).group(0)
                day = actual.split(' ')[0]
                part = tmp.split(day)[1]
                if day=='Today':
                    day_string = str(date.today())
                elif day=='Yesterday':
                    day_string = str(date.today()-timedelta(days=1))
                else:
                    day_string = str(day)
                b = time.strptime(day_string+part, '%Y-%m-%d %I:%M %p')
            elif re.search(v2, tmp, re.IGNORECASE):
                
                actual = re.search(v2, tmp, re.IGNORECASE).group(0)
                day = actual.split(',')[0]
                part = tmp.split(day)[1]
                if day=='Today':
                        day_string = str(date.today())
                elif day=='Yesterday':
                        day_string = str(date.today()-timedelta(days=1))
                else:
                    day_string = str(day)
                b = time.strptime(day_string+part, '%Y-%m-%d, %I:%M %p')
            #print day_string+part
            elif re.search(d2, tmp, re.IGNORECASE):
                actual = re.search(d2, tmp, re.IGNORECASE).group(0)
                day = actual.split(' ')[0]
                part = tmp.split(day)[1]
                if day=='Today':
                    day_string = str(date.today())
                elif day=='Yesterday':
                    day_string = str(date.today()-timedelta(days=1))
                else:
                    day_string = str(day)
                b = time.strptime(day_string+part, '%Y-%m-%d at %I:%M:%S %p')
            elif re.search(d3, tmp, re.IGNORECASE):
                tmp = re.sub(u'\xa0',' ',tmp)
                actual = re.search(d3, tmp, re.IGNORECASE).group(0)
                day = actual.split(' ')[0]
                part = tmp.split(day)[1]
                if day=='Today':
                    day_string = str(date.today())
                elif day=='Yesterday':
                    day_string = str(date.today()-timedelta(days=1))
                else:
                    day_string = str(day)
                retv = re.sub(',','',day_string+part)
                try:
                    b = time.strptime(retv, '%m-%d-%Y %I:%M %p')
                except ValueError:
                    b = time.strptime(retv, '%m-%d-%Y %I:%M %p')
            elif tmp.find('Last Activity:')>-1:
                #pass
                temp = tmp.split('Last Activity:')[1].strip()
                try:
                    b = time.strptime(temp, '%m-%d-%Y, %I:%M %p')
                except ValueError:
                    b = time.strptime(temp, '%m-%d-%Y %I:%M %p')
                    
            elif tmp.find('Posted:')>-1:
                temp = tmp.split()
            elif re.match(d2, tmp, re.IGNORECASE):
                b = time.strptime(tmp, '%m-%d-%Y, %I:%M %p')
            
            else:
                tmp = re.sub(',','',tmp)
                try:
                    b = time.strptime(tmp, '%B %d %Y %I:%M:%S %p')
                except ValueError:
                    #try:
                    b = time.strptime(tmp, '%m-%d-%Y\xa0%I:%M %p')
                    
            of = time.strftime('%m-%d-%Y %H:%M',b)
            return of
        
    def get_handle(self, tmp):
        if tmp:
            return tmp.strip()

    def convert_to_valid_date(self, dday):
        try:
            dday = re.sub(',','',dday)
            try:
                g = time.strptime(dday, '%m-%d-%Y %H:%M')
            except ValueError:
                try:
                    g = time.strptime(dday, '%m-%d-%Y %I:%M %p')
                except ValueError:
                    try:
                        g = time.strptime(dday, '%b %d %Y')
                    except ValueError:
                        try:
                            g = time.strptime(dday, '%a %b %d %Y %I:%M %p')
                        except ValueError:
                            g = time.strptime(dday, '%B %d %Y %I:%M:%S %p')
            t = time.strftime('%Y-%m-%dT%H:%M',g)
        except ValueError:
            g = time.strptime(dday, '%m-%d-%Y')
            t = time.strftime('%Y-%m-%d',g)
        return t
    
    def thread_ID(self, tmp):
        if tmp:
            tmp = tmp.split('showthread.php?')[1]
            tmp = tmp.split('-')[0]
            return tmp
    
if __name__=='__main__':
    df = '01-14-2011 03:22 PM'
    vw = vwvortex()
    print vw.last_activity(df)