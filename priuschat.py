import re
from datetime import date, timedelta
import time
PRIUSCHAT = 'http://priuschat.com/forums/'
class priuschat:
    ####->>>>>>>>>>> I am here
    def __init__(self):
        self.domain = PRIUSCHAT
        self.main_cat = "(//span[@class='navbar'])[last()]"
        self.cur_cat = "//td/font/strong"
        self.linklist = "//*[@class='alt1Active' or @class='subforum']//a[not(contains(@href,'/shop')) and not(contains(@href,'/groups') and not(contains(@href,'hybridchat.com'))) and contains(@href,'forums/')]/@href"
        self.threads_list = "//a[contains(@id,'thread_title')]/@href"
        self.next_link = "(//a[@class='smallfont' and contains(@title,'Next Page')]/@href)[1]"
        self.member_list_url = "http://priuschat.com/forums/members/list"
        self.member_list = "//td[@class='alt1Active']/a/@href"
        #self.something = "//tbody[starts-with(@id,'collapseobj_forumbit')]/tr[not(contains(./td[@class='alt1'],'-'))]"
        self.threaddata = "//tbody[starts-with(@id,'threadbits_forum')]/tr"
        self.description = ".//a[contains(@id,'thread_title')]"
        self.replies = ".//td[@class='alt1'][last()]"
        self.views = ".//td[@class='alt2'][last()]"
        self.link = ".//td//a[contains(@id,'thread_title')]/@href"
        self.postdata = "//table[starts-with(@id,'post')]"
        self.timeofpost =".//td[@class='thead' and not(@align)]"  #this needs to be parsed further in order to extract the time of the post
        self.posterid = ".//a[@class='bigusername']/@href" #needs to be parsed to get the poster id
        self.postid = ".//a[starts-with(@id,'postcount')]/@href" #needs to be parsed to get the post id
        self.postcount =".//a[starts-with(@id,'postcount')]/@name" 
        self.postlink = ".//a[starts-with(@id,'postcount')]/@href" 
        self.post_thread = "" #this is not a number
        
        self.location =  "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Location')]/following-sibling::*[1]"
        self.name = ""
        self.cars = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Your')]/following-sibling::*[1]"
        self.handle = "//td[@id='username_box']/h1"
        self.interests = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Interests')]/following-sibling::*[1]"
        self.noposts = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Total Posts:')]"
        self.lastac = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Last Activity:')]"
        self.joindate = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Join Date:')]"
        self.plus_fb = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Total Thanks:')]"
        self.minus_fb = "//table[@class='tborder']//td[@class='alt1']//td[contains(.,'Total negative feedback:')]/following-sibling::*"
        self.ppday = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Posts Per Day:')]" #this needs a little more programming
        self.bio = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Biography')]/following-sibling::*[1]"
        self.occupation = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Occupation')]/following-sibling::*[1]"
        self.ulink = "//div[@id='profile_tabs']//dl[@class='list_no_decoration']//dt[contains(.,'This Page')]/following-sibling::*[1]/a"
        self.userid = ""
        
    def thread_id(self, tmp):
        tmp_ls = tmp.split('/')[-1]
        tmpy = tmp_ls.split('-')[0]
        return tmpy

    def post_id(self, tmp):
#        print tmp
        return tmp.split('#post')[1]
    
    def poster_id(self, tmp):
#        print tmp
        return tmp.split('/')[-1].split('.')[0]

    def total_posts(self,tmp):
        if tmp:
            return re.sub(',','',tmp.split(':')[1].strip())
    
    def last_activity(self, tmp):
            v1 = r'[yester|to]+day[\s]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            v2 = r'[yester|to]+day[\s|\,\s|\s\,]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            d1 = r'[\d]{2}-[\d]{2}-[\d]{4}[\s|\,\s]{1}[\d]{2}:[\d]{2}'
            d3 = r'[\d]{2}-[\d]{2}-[\d]{4}[\s|\,\s]{2}[\d]{2}:[\d]{2}[\s]+[AM|PM]+'
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
                b = time.strptime(tmp, '%B %d %Y %I:%M:%S %p')
            of = time.strftime('%m-%d-%Y %H:%M',b)
            return of

    
    def join_date(self, tmp):
        if tmp:
            return tmp.split(':')[1].strip()

    def p_p_day(self, tmp):
        if tmp:
            return tmp.split(':')[1].strip()
        
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
