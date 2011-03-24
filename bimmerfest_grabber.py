#from config import *
import pdb
from bimmerfest import *
import re
import time
from DBManager import DBManager
from utils import *
from config import *
def bimmerfest_user_grab(url,userdb = 'bimmerfest_users', debug = True):
    bimm = bimmerfest()
    main_page = xmlTree(url)
    userdata = []
    if main_page:
                if not debug:
                    udb = DBManager()
                
                if len(main_page.xpath(bimm.location))>0:
                    userdata.append(('Location',re.escape(main_page.xpath(bimm.location)[0].text_content())))
            #        print main_page.xpath(bimm.location)[0].text_content()
                if len(main_page.xpath(bimm.cars))>0:
            #        print main_page.xpath(bimm.cars)[0].text_content()
                    userdata.append(('Cars',re.escape(main_page.xpath(bimm.cars)[0].text_content())))  
                if len(main_page.xpath(bimm.interests))>0:
                    #print main_page.xpath(bimm.interests)[0].text_content()
                    userdata.append(('Interests',re.escape(main_page.xpath(bimm.interests)[0].text_content())))
                if len(main_page.xpath(bimm.noposts))>0:
                    #print bimm.total_posts(main_page.xpath(bimm.noposts)[0].text_content())
                    userdata.append(('TotalPosts',bimm.total_posts(main_page.xpath(bimm.noposts)[0].text_content())))
                if len(main_page.xpath(bimm.lastac))>0:
                    #print bimm.last_activity(main_page.xpath(bimm.lastac)[0].text_content())
                    userdata.append(('LastActivity',bimm.convert_to_valid_date(bimm.last_activity(main_page.xpath(bimm.lastac)[0].text_content()))))
                if len(main_page.xpath(bimm.joindate))>0:
                    #print bimm.join_date(main_page.xpath(bimm.joindate)[0].text_content())
                    userdata.append(('JoinDate',bimm.convert_to_valid_date(bimm.join_date(main_page.xpath(bimm.joindate)[0].text_content()))))
                if len(main_page.xpath(bimm.ppday))>0:
                    #print bimm.p_p_day(main_page.xpath(bimm.ppday)[0].text_content())
                    userdata.append(('PostsPerDay',bimm.p_p_day(main_page.xpath(bimm.ppday)[0].text_content())))
                if len(main_page.xpath(bimm.handle))>0:
                    #print main_page.xpath(bimm.handle)[0].text_content()
                    userdata.append(('Handle',re.escape(main_page.xpath(bimm.handle)[0].text_content())))
                if len(main_page.xpath(bimm.bio))>0:
                    #print main_page.xpath(bimm.bio)[0].text_content()
                    userdata.append(('Biography',re.escape(main_page.xpath(bimm.bio)[0].text_content())))
                
                if len(main_page.xpath(bimm.occupation))>0:
                    #print main_page.xpath(bimm.occupation)[0].text_content()
                    userdata.append(('Occupation',main_page.xpath(bimm.occupation)[0].text_content()))
            
                if len(main_page.xpath(bimm.ulink))>0:
                    #print main_page.xpath(bimm.ulink)[0].text_content()
                    userdata.append(('Link',main_page.xpath(bimm.ulink)[0].text_content()))
            #      print userdata
                if not debug:
                    udb.insert_into_table(userdb, userdata)
                    udb.close() #@IndentOk
                else:
                    print userdata
    else:
        pass
def bimmerfest_thread_grab(url,postsdb='bimmerfest_posts', debug = True):
    #print "ceva"
    bimm = bimmerfest()
    next_page = xmlTree(url)
    #posts = main_page
    if not debug:
        udb = DBManager()
    while True:
        try:
            next = next_page.xpath(bimm.next_link)[0]
        except IndexError:
            next = None
        posts = next_page.xpath(bimm.postdata)
        for t in posts:
            if t.xpath(bimm.posterid):
                threaddata = [] 
                #print '**********************************************************************'
                #print t.xpath(bimm.timeofpost)[0].text_content().strip()
                threaddata.append(('TimeOfPost',bimm.convert_to_valid_date(bimm.last_activity(t.xpath(bimm.timeofpost)[0].text_content().strip()))))
                #print bimm.poster_id(t.xpath(bimm.posterid)[0])#[0].text_content()
                threaddata.append(('PosterID',bimm.poster_id(t.xpath(bimm.posterid)[0])))#[0].text_content()))
                #print bimm.post_id(t.xpath(bimm.postid)[0])#[0].text_content()
                threaddata.append(('PostID',bimm.post_id(t.xpath(bimm.postid)[0])))
                #print t.xpath(bimm.postcount)[0].text_content()
                threaddata.append(('PostCountInThread', t.xpath(bimm.postcount)[0].text_content()))
                #print t.xpath(bimm.postlink)#[0].text_content()
                threaddata.append(('Link',t.xpath(bimm.postlink)[0]))
                threaddata.append(('ThreadID',bimm.thread_id(t.xpath(bimm.post_thread)[0])))
                bimmerfest_user_grab(bimm.domain+t.xpath(bimm.posterid)[0], 'bimmerfest_users')
                if not debug:
                    udb.insert_into_table(postsdb, threaddata)
                else:
                    print threaddata
                #print '**********************************************************************'
        if next:
            next_page = xmlTree(bimm.domain+next+alltime)
            
        elif not next:
            if not debug:
                udb.close()
            else:
                pass
            break

def bimmerfest_grab(threaddb = 'bimmerfest_threads', debug = True):
    bmw = bimmerfest()
    main_page = xmlTree(bmw.domain)
    lvl1 = main_page.xpath(bmw.linklist)
    if not debug:
        udb = DBManager()
    for lvl1_link in lvl1:
        #print lvl1_link
        next_page = xmlTree(bmw.domain+lvl1_link+alltime)
        #next_page = xmlTree(lvl1_link)
        print bmw.domain+lvl1_link
        #next = next_page.xpath(bmw.next_link)[0]
        while True:
            try:
                next = next_page.xpath(bmw.next_link)[0]
            except IndexError:
                next = None
            threads = next_page.xpath(bmw.threads_list)
            tread_data = next_page.xpath(bmw.threaddata)
            for j in tread_data:
                #pass
                threaddata = []
                if j.xpath(bmw.description):
                    threaddata.append(('Description', j.xpath(bmw.description)[0].text_content().encode('utf-8')))
                    #print j.xpath(bmw.description)[0].text_content().encode('utf-8')
                    threaddata.append(('Replies', j.xpath(bmw.replies)[0].text_content()))
                    #print j.xpath(bmw.replies)[0].text_content()
                    threaddata.append(('Views', j.xpath(bmw.views)[0].text_content()))
                    #print j.xpath(bmw.views)[0].text_content()
                    threaddata.append(('Link', j.xpath(bmw.link)[0]))
                    #print j.xpath(bmw.link)[0]
                    if not debug:
                        udb.insert_into_table(threaddb, threaddata)
                    else:
                        print threaddata
                    bimmerfest_thread_grab(bmw.domain+j.xpath(bmw.link)[0])
                    
            for k in threads:
                pass
                #                print k
            if next:
                next_page = xmlTree(bmw.domain+next+alltime)
            
            elif not next:
                break
    if not debug:
        udb.close()
bimmer_user = 'http://www.bimmerfest.com/forums/member.php?u=210815'
bimmerfest_thrd = 'http://www.bimmerfest.com/forums/showthread.php?t=324446'
bimmerg = 'http://www.bimmerfest.com/forums/showthread.php?t=514868'
threads = Fields(thread_table_fields, 'threads')
posts = Fields(posts_table_fields, 'posts')
users = Fields(user_table_fields, 'users')
if __name__=='__main__':
    #bf = bimmerfest()
    #bimmerfest_thread_grab(bimmerfest_thrd)
#    dbf = DBManager()
#    dbf.create_tables('bimmerfest', 'users', users)
#    dbf.create_tables('bimmerfest', 'threads', threads)
#    dbf.create_tables('bimmerfest', 'posts', posts)
#    bimmerfest_grab()
    #bimmerfest_user_grab(bimmer_user)
    bimmerfest_thread_grab(bimmerfest_thrd)