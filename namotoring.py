import re
from datetime import date, timedelta
import time
NAMOTORING = 'http://www.northamericanmotoring.com/forums/'

class namotoring:
    
    def __init__(self):
        self.domain = NAMOTORING
        self.main_cat = "(//span[@class='navbar'])[last()]"
        self.cur_cat = "//td/font/strong"
        self.linklist = "//*[@class='alt1Active' or @class='subforum']//a[not(@target)]/@href"
        self.threads_list ="//a[contains(@id,'thread_title')]/@href"
        self.next_link = "(//a[@class='smallfont' and contains(@title,'Next Page')]/@href)[1]"
        self.member_list_url = "http://www.northamericanmotoring.com/forums/members/list/"
        self.member_list = "//tr[@align='center']/td[@class='alt1Active']/a/@href"
        self.threaddata = "//tbody[contains(@id,'threadbits_forum')]/tr"
        self.description = ".//a[contains(@id,'thread_title')]"
        self.replies = ".//td[@class='alt1'][last()]"
        self.views = ".//td[@class='alt2'][last()]"
        self.link = ".//td//a[contains(@id,'thread_title')]/@href"
        self.postdata = "//table[starts-with(@id,'post')]"
        self.timeofpost =".//td[@class='thead']//div[@class='normal' and not(@style)]"  #this needs to be parsed further in order to extract the time of the post
        self.posterid = ".//a[@class='bigusername']/@href" #needs to be parsed to get the poster id
        self.postid = ".//a[starts-with(@id,'postcount')]/@href" #needs to be parsed to get the post id
        self.postcount =".//a[starts-with(@id,'postcount')]/@name" 
        self.postlink = ".//a[starts-with(@id,'postcount')]/@href" 
        self.post_thread = "//link[@rel='canonical']/@href"
        self.location = "//div[@class='fieldset']//tr//td[contains(.,'Location')]"
        self.name = ""
        self.cars = ""
        self.handle = "//div[@class='bigusername']"
        self.interests = "normalize-space(substring-after(//div[@class='fieldset']//td[contains(.,'Interests')],':'))"
        self.noposts = "//td[@class='panelsurround']//fieldset//td[contains(.,'Total Posts:')]"
        self.lastac = "//td[@class='smallfont']/div"
        self.joindate = "//td[@class='panelsurround']//div[@style and contains(.,'Join Date:')]"
        self.plus_fb = "//table[@class='tborder']//td[@class='alt1']//td[contains(.,'Total positive feedback:')]/following-sibling::*"
        self.minus_fb = "//table[@class='tborder']//td[@class='alt1']//td[contains(.,'Members who left negative:')]/following-sibling::*"
        #self.ppday = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//li[contains(.,'Posts Per Day:')]" this needs a little more programming
        #self.bio = "//div[@id='profile_tabs']//ul[@class='list_no_decoration']//dt[contains(.,'Biography')]/following-sibling::*[1]"
        self.occupation = "//div[@class='fieldset']//td[contains(.,'Occupation')]/text()"
        self.ulink = "//div[@id='profile_tabs']//dl[@class='list_no_decoration']//dt[contains(.,'This Page')]/following-sibling::*[1]/a"
        self.userid = ""
        self.name = "//a[starts-with(@href,'mailto:')]/@href"
    
    def thread_id(self, tmp):
        return tmp.split('&t=')[1]

    def post_id(self, tmp):
        #print tmp
        return tmp.split('/')[-1].split('-')[0]
    
    def poster_id(self, tmp):
        #print tmp
        return tmp.split('/')[-1].split('-')[0]
    
    def time_of_post(self, tmp):
        pass
    
    def total_posts(self, tmp):
        #print tmp.strip()
        total = tmp.split('(')[0]
        ppd = tmp.split('(')[1]
        total = total.split(':')[1].strip()
        ppd = ppd.split('posts')[0].strip()
        return re.sub(',','',total),ppd
    def join_date(self, tmp):
        if tmp:
            return tmp.split(':')[1].strip()

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
                b = time.strptime((day_string+part).strip(), '%Y-%m-%d %I:%M %p')
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

    def get_name_email(self, tmp):
        if tmp:
            minim =  tmp.split(':')[1]
            nm = minim.split('@')[0]
            return nm
        else:
            return 'None'
    
    def get_location(self, tmp):
        if tmp:
            return tmp.split(':')[1].strip()
        
#    def get_feedback(self, tmp):
#        if tmp:
#            
    
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

if __name__=='__main__':
    bi = namotoring()
    dt = '12-28-2004, 06:04 PM'
    print bi.last_activity(dt)