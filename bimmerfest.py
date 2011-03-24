import re
from datetime import date, timedelta
import time
BIMMERFEST = 'http://www.bimmerfest.com/forums/'

class bimmerfest:

    def __init__(self):
        self.domain = BIMMERFEST
        self.main_cat = "(//span[@class='navbar'])[last()]"
        self.cur_cat = "//td[@class='navbar']"
        #self.main_categories = "//td[@class='tcat']//a[starts-with(@href,'forumdisplay.php')]/@href"
        self.linklist = "//td[not(@class='tcat')]//a[starts-with(@href,'forumdisplay.php') and not(contains(@href,'do=markread'))]/@href"
        #self.first_level_subcategories = 
        self.threads_list = "//a[contains(@id,'thread') and not(contains(@id,'gotonew'))]/@href"
        self.next_link = "(//a[@class='smallfont' and contains(@title,'Next Page')]/@href)[1]" #is global
        self.member_list_url = "http://www.bimmerfest.com/forums/memberlist.php"
        self.member_list = "//a[contains(@href,'member.php?')]/@href"
#        self.subforums_loop = "//a[starts-with(@href,'forumdisplay.php')]/strong"
#        self.subforums_list = "(//a[contains(.,(//a[starts-with(@href,'forumdisplay.php')]/strong)[%s])])[1]"
        self.threaddata = "//tbody[contains(@id,'threadbits_forum')]/tr"
        self.description = ".//a[contains(@id,'thread_title')]"
        self.replies = ".//td[@class='alt1'][last()]"
        self.views = ".//td[@class='alt2'][last()]"
        self.link = ".//td//a[contains(@id,'thread_title')]/@href"
        self.postdata = "//table[starts-with(@id,'post')]"
        self.timeofpost = ".//div[@class='normal' and not(@style)]"
        self.posterid = ".//div[starts-with(@id,'postmenu_')]/a/@href" #needs to be parsed in order to get the posterid
        self.postid = ".//div[@class='normal']/a[starts-with(@id,'postcount')]/@href" #needs to be parsed in order to get the post id
        self.postcount = ".//div[@class='normal']/a[starts-with(@id,'postcount')]"
        self.postlink = ".//div[@class='normal']/a[starts-with(@id,'postcount')]/@href"
        #self.posterdata = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']"
        self.location = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Location')]/following-sibling::*[1]"
        self.post_thread = "(//a[starts-with(@href,'showthread.php')]/@href)[1]"
        self.name = ""
        self.handle = "//td[@id='username_box']/h1"
        self.cars = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'What I drive')]/following-sibling::*[1]"
        
        self.interests = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Interests')]/following-sibling::*[1]"
        self.noposts = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Total Posts:')]"
        self.lastac = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Last Activity:')]"
        self.joindate = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Join Date:')]"
        self.plus_fb = ""
        self.minus_fb = ""
        self.ppday = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Posts Per Day:')]"
        self.bio = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Biography')]/following-sibling::*[1]"
        self.occupation = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Occupation')]/following-sibling::*[1]"
        self.ulink = "//div[@id='profile_tabs']//dl[@class='list_no_decoration']//dt[contains(.,'This Page')]/following-sibling::*[1]/a"
        self.userid = ""

    def convert_to_valid_date(self, dday):
        try:
            dday = re.sub(',','',dday)
            try:
                g = time.strptime(dday, '%m-%d-%Y %H:%M')
            except ValueError:
                g = time.strptime(dday, '%m-%d-%Y %I:%M %p')
            t = time.strftime('%Y-%m-%dT%H:%M',g)
        except ValueError:
            g = time.strptime(dday, '%m-%d-%Y')
            t = time.strftime('%Y-%m-%d',g)
        return t

    def convert_post_time(self, dday):
        try:
            g = time.strptime(dday.strip(), '%m-%d-%Y, %I:%M %p')
            t = time.strftime('%Y-%m-%dT%H:%M',g)
        except ValueError:
            pass
        return t

    def thread_id(self, tmp):
        if tmp.find('&t=')!= -1:
            tmp = tmp.split('&t=')[1]
            if tmp.find('&')!= -1:
                tmp = tmp.split('&')[0]
            return tmp
        elif tmp.find('?t=')!= -1:
            tmp = tmp.split('?t=')[1]
            if tmp.find('&')!= -1:
                tmp = tmp.split('&')[0]
            return tmp
        else:
            pass

    def poster_id(self, tmp):
        if tmp:
            return tmp.split('&u=')[1]

    def post_id(self, tmp):
        if tmp:
            return tmp.split('&p=')[1].split('&')[0]

    def total_posts(self, tmp):
        if tmp:
            return re.sub(',','',tmp.split('Posts:')[1].strip())
    
    def join_date(self, tmp):
        if tmp:
            return tmp.split('Date:')[1].strip()

#    def total_posts(self, tmp):
#            if tmp:
#                    return tmp.split(':')[1].strip()
######### Trebuie o functie entru pagina user si una pentru cea post
    def last_activity(self, tmp):
            #tmp = re.sub(u'\\xa',' ',tmp)
            tmp = tmp.strip()
            #print tmp
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
                    b = time.strptime(tmp, '%m-%d-%Y\xa0%I:%M %p')
            of = time.strftime('%m-%d-%Y %H:%M',b)
            return of
#    def join_date(self, tmp):
#            if tmp:
#                    return tmp.split(':')[1].strip()

    def p_p_day(self, tmp):
        if tmp:
            return tmp.split('Day:')[1].strip()
        
bimmer_user = 'http://www.bimmerfest.com/forums/member.php?u=210815'     
        
if __name__=='__main__':
    y = bimmerfest()
    la = 'Last Activity: 09-30-2010 10:10 PM'
    lav = 'Last Activity: Today 10:10 PM'
    print y.last_activity(la)
    print y.last_activity(lav)
    
