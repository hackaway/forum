import re
from datetime import date, timedelta
import time
MAZDA3 = 'http://www.mazda3forums.com/'

class mazda3:
    
    def __init__(self):
        self.domain = MAZDA3
        self.main_cat = "(//div[@class='navigate_section']/ul/li[last()]-1)[1]"
        self.cur_cat = "(//div[@class='navigate_section']/ul/li[last()])[1]"
        self.linklist = "//td[@class='children windowbg' or @class='info']/a[not(contains(.,'.com'))]/@href"
        self.threads_list = "//span[starts-with(@id,'msg_')]/a/@href"
        self.next_link = ""
        self.last_page_threads = "(//a[@class='navPages'])[last()]"
        
        self.member_list_url = "http://www.mazda3forums.com/index.php?action=mlist"
        self.member_list = "//a[contains(@href,'action=profile') and @title]/@href"

        self.threaddata = "//table[@class='table_grid']/tbody/tr[not(@class='titlebg')]"
        self.description = ".//span[starts-with(@id,'msg_')]"
        #self.views = ".//td[starts-with(@class,'stats')]"
        #self.replies = "(.//span[@class='postdetails'])[2]"
        self.stats = ".//td[starts-with(@class,'stats')]"
        self.link = ".//span[starts-with(@id,'msg_')]/a/@href"
        
        self.postdata = "//div[@class='post_wrapper']"
        self.timeofpost =".//div[@class='keyinfo']/div[@class='smalltext']"  #this needs to be parsed further in order to extract the time of the post
        self.posterid = ".//div[@class='poster']/h4/a/@href" #needs to be parsed to get the poster id
        self.postid = ".//div[@class='keyinfo']/h5[starts-with(@id,'subject_')]/a/@href" #needs to be parsed to get the post id
        self.postcount =".//div[@class='keyinfo']/div[@class='smalltext']/strong[not(contains(.,'Yesterday')) and not(contains(.,'Today'))]" #needs some programming
        self.postlink = ".//div[@class='keyinfo']/h5[starts-with(@id,'subject_')]/a/@href"
        self.post_thread = "//link[@rel='canonical']/@href"
        self.handle = "//div[@class='username']/h4/text()"
        self.car_make = "//div[@id='detailedinfo']//div[@class='content']//dt[contains(.,'Car Make')]/following-sibling::dd[1]"
        self.car_year = "//div[@id='detailedinfo']//div[@class='content']//dt[contains(.,'Car Make')]/following-sibling::dd[2]"
        self.location = "//div[@class='content']//dt[contains(.,'Location')]/following-sibling::*"
        self.noposts = "//div[@class='content']//dt[contains(.,'Mazda3Forums Posts')]/following-sibling::*[1]"
        self.ppday = "//div[@class='content']//dt[contains(.,'Total Posts')]/following-sibling::*[1]"
        self.plus_fb = "//div[@class='content']//dt[contains(.,'Positive Feedback')][2]/following-sibling::*[1]"
        self.minus_fb = "//div[@class='content']//dt[contains(.,'Negative Feedback')]/following-sibling::*[1]"
        self.joindate = "//div[@class='content']//dt[contains(.,'Date Registered')]/following-sibling::*[1]"
        self.lastac = "//div[@class='content']//dt[contains(.,'Last Active')]/following-sibling::*[1]"

    
    def parse_stats(self, content):
        tmp = content.split('\n')
        tmp_ls = []
        stats = {}
        for k in tmp:
            if re.sub('\t','',k) != '':
                tmp_ls.append(re.sub('\t','',k))
        stats['Views'] = tmp_ls[1].split(' ')[0]
        stats['Replies'] = tmp_ls[0].split(' ')[0]
        return stats

    def thread_id(self, tmp):
        return tmp.split('&topic=')[1].split('.')[0]    

    def post_id(self, tmp):
         #print tmp       
        return tmp.split('#msg')[1]
                
    def poster_id(self, tmp):
         #print tmp      
        return tmp.split(';u=')[1].split('-')[0]

    def time_of_post(self ,tmp):
            #print tmp
            return (tmp.split('on: ')[1])[:-2]
        
    def post_count(self, tmp):
        if tmp.split(' ')[1].strip('#')=='on:':
            return '1'
        else:
            return str(int(tmp.split(' ')[1].strip('#'))+1)
        
    def total_posts(self, tmp):
        return tmp
    
    def get_handle(self, tmp):
        if tmp:
            return tmp 
    
        
    def join_date(self, tmp):
        if tmp:
            return tmp

    def get_car(self, tmp1, tmp2):
        return tmp1+' '+tmp2
    
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
    
    def last_activity(self, tmp):
            v1 = r'[yester|to]+day[\s]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            v2 = r'[yester|to]+day[\s|\,\s|\s\,]+[\d]{2}[:][\d]{2}[\s]+[AM|PM]+'
            d1 = r'[\d]{2}-[\d]{2}-[\d]{4}[\s|\,\s]{1}[\d]{2}:[\d]{2}'
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
        
if __name__=='__main__':
    dt = 'Today at 12:04:08 am'
    bimm = mazda3()
    print bimm.last_activity(dt)