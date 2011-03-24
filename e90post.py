import re
from datetime import date, timedelta
import time
E90POST = 'http://www.e90post.com/forums/'
class e90post:

    def __init__(self):
        self.domain = E90POST
        self.main_cat = "(//span[@class='navbar'])[last()]"
        self.cur_cat = "//td/font/strong"
        self.linklist = "//td[not(@class='tcat')]//a[starts-with(@href,'forumdisplay.php') and not(contains(@href,'do=markread')) and not(contains(.,'M3 Forum'))]"
        #self.threads_list =
        self.next_link = "(//a[@class='smallfont' and contains(@title,'Next Page')]/@href)[1]"
        self.member_list_url = "http://www.e90post.com/forums/memberlist.php"
        self.member_list = "//a[contains(@href,'member.php?')]"
        self.threads_list = "//a[contains(@id,'thread') and not(contains(@id,'gotonew'))]/@href"
        #pass
        self.threaddata = "//tbody[contains(@id,'threadbits_forum')]/tr"
        self.description = ".//a[contains(@id,'thread_title')]"
        self.replies = ".//td[@class='alt1'][last()]"
        self.views = ".//td[@class='alt2'][last()]"
        self.link = ".//td//a[contains(@id,'thread_title')]/@href"
        self.postdata = "//table[starts-with(@id,'post')]"
        self.timeofpost =".//td[@class='thead' and not(@align)]" 
        self.posterid = ".//a[@class='bigusername']/@href" #needs to be parsed to get the poster id
        self.postid = ".//a[starts-with(@id,'postcount')]/@href" #needs to be parsed to get the post id
        self.postcount =".//a[starts-with(@id,'postcount')]/@name" 
        self.postlink = ".//a[starts-with(@id,'postcount')]/@href" 
        self.post_thread = "//td[@id='threadtools']/a/@href"
        #//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Car')]/following-sibling::*[1]
        self.location = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Location')]/following-sibling::*[1]"
        #self.name = ""
        self.cars = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Car')]/following-sibling::*[1]"
        self.handle = "//td[@id='username_box']/h1"
        self.interests = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Interests')]/following-sibling::*[1]"
        self.noposts = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Total Posts:')]"
        self.lastac = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Last Activity:')]"
        self.joindate = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Join Date:')]"
        self.plus_fb = ""
        self.minus_fb = ""
        self.ppday = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Posts Per Day:')]"
        self.bio = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Biography')]/following-sibling::*[1]"
        self.occupation = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Occupation')]/following-sibling::*[1]"
        self.ulink = "//div[@id='profile_tabs']//dt[contains(.,'This Page')]/following-sibling::*[1]/a"
        self.userid = ""
	

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
    
    def post_id(self, tmp):
#        print tmp
        return tmp.split('&p=')[1].split('&post')[0]
    
    def poster_id(self, tmp):
        #print tmp
        return tmp.split('&u=')[1]

    def total_posts(self, tmp):
        if tmp:
            return re.sub(',','',tmp.split(':')[1].strip())

    def last_activity(self, tmp):
            v1 = r'[yester|to]+day[\s]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            v2 = r'[yester|to]+day[\s|\,\s|\s\,]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            d1 = r'[\d]{2}-[\d]{2}-[\d]{4}[\s|\,\s]{1}[\d]{2}:[\d]{2}'
            d2 = r''
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
            elif tmp.find('Last Activity:')>-1:
                #pass
                temp = tmp.split('Last Activity:')[1].strip()
                try:
                    b = time.strptime(temp, '%m-%d-%Y, %I:%M %p')
                except ValueError:
                    b = time.strptime(temp, '%m-%d-%Y %I:%M %p')
            elif re.match(d2, tmp, re.IGNORECASE):
                b = time.strptime(tmp, '%m-%d-%Y, %I:%M %p')
            
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
                g = time.strptime(dday, '%m-%d-%Y %I:%M %p')
            t = time.strftime('%Y-%m-%dT%H:%M',g)
        except ValueError:
            g = time.strptime(dday, '%m-%d-%Y')
            t = time.strftime('%Y-%m-%d',g)
        return t