import re
from datetime import date, timedelta
import time
FEOA = 'http://www.feoa.net/'#modules.php?name=forums'

class feoa:
    
    def __init__(self):
        self.domain = FEOA
        self.main_cat = "//a[@class='nav'][1]"
        self.cur_cat = "//a[@class='nav'][2]"
        self.linklist = "//a[@class='mforumlink']/@href"
        self.threads_list = "//a[@class='topictitle']/@href"
        self.next_link = "//span[@class='gensmall']//a[contains(.,'Next')]/@href"
        
        self.member_list_url = "http://www.feoa.net/modules.php?name=Members_List"
        self.member_list = "//td[@class='row1']/span[@class='gen']/a/@href"
        
        self.threaddata = "//table[@class='forumline']//tr"
        self.description = ".//span[@class='topictitle']"
        self.replies = "(.//span[@class='postdetails'])[1]"
        self.views = "(.//span[@class='postdetails'])[2]"
        self.link = ".//a[@class='topictitle']/@href"

        self.postdata = "//td[@class='postline' and not(@width)]"
        self.timeofpost =".//span[@class='gensr' and contains(.,'Posted')]"  #this needs to be parsed further in order to extract the time of the post
        self.posterid = ".//td[@valign='middle']/a[1]/@href" #needs to be parsed to get the poster id
        self.postid = ".//td[@width]/a/@href" #needs to be parsed to get the post id
        self.postcount =".//a[starts-with(@id,'postcount')]/@name" #needs some programming
        self.postlink = ".//td[@width]/a/@href"
        self.post_thread = "(//a[starts-with(@href,'modules.php?') and contains(@href,'t=')]/@href)[2]"

        #self.ulink  = ""
        self.handle = "(//td[@class='catLeft']/b/span[@class='gen'])[2]"
        self.joindate = "//td[@class='postfr']//td[contains(.,'Joined')]/following-sibling::*"
        self.lastac = "//td[@class='postfr']//td[contains(.,'Last Visit')]/following-sibling::*"
        self.noposts = "//td[@class='postfr']//td[contains(.,'Total posts')]/following-sibling::*" # needs more porgramming to get the data for posts and the frequency
        self.location = "//td[@class='postfr']//td[contains(.,'Location')]/following-sibling::*"
        self.occupation = "//td[@class='postfr']//td[contains(.,'Occupation')]/following-sibling::*"
        self.interests = "//td[@class='postfr']//td[contains(.,'Interests')]/following-sibling::*"
        #self.ppday = "//ul[@class='list_no_decoration']/li[contains(.,'Posts Per Day')]/text()"
        
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
                
        return tmp.split('#')[1]
                
    def poster_id(self, tmp):
               
        return tmp.split('&u=')[-1]

    def time_of_post(self, tmp):
        return tmp.split('Posted:')[1].strip()
    #def total_posts(self, tmp):
    #    print tmp

    def total_posts(self, tmp):
        #print tmp.strip()
        total = tmp.split('[')[0]
        ppd = tmp.split('[')[1]
        #total = total.split(':')[1].strip()
        ppd = ppd.split('/')[1].split('posts')[0].strip()
        return total,ppd

    def join_date(self, tmp):
        if tmp:
            return tmp.strip()

    #def p_p_day(self, tmp):
    #    print tmp

    def last_activity(self, tmp):
        if tmp:
            return tmp.strip()

    def get_handle(self, tmp):
        if tmp:
            return tmp.split('about')[1].strip()
    
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
                        g = time.strptime(dday, '%a %b %d %Y %I:%M %p')
            t = time.strftime('%Y-%m-%dT%H:%M',g)
        except ValueError:
            g = time.strptime(dday, '%m-%d-%Y')
            t = time.strftime('%Y-%m-%d',g)
        return t