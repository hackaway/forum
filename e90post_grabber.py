'''
Created on Jan 25, 2011

@author: arturd
'''
from utils import *
from e90post import *
from DBManager import DBManager
from config import *
def e90post_user_grab(url, userdb='e90post_users', debug = True):
    bimm = e90post()
    main_page = xmlTree(url)
    userdata = []
    #pdb.set_trace()
    if main_page:
            if not debug:
                udb = DBManager()
            if len(main_page.xpath(bimm.location))>0:
                #print main_page.xpath(bimm.location)[0].text_content().strip()
                userdata.append(('Location',main_page.xpath(bimm.location)[0].text_content().strip()))
                #if len(main_page.xpath(bimm.cars))>0:
                #  print main_page.xpath(bimm.cars)[0].text_content()
            if len(main_page.xpath(bimm.interests))>0:
                #print main_page.xpath(bimm.interests)[0].text_content()
                userdata.append(('Interests',main_page.xpath(bimm.interests)[0].text_content()))
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
                #if len(main_page.xpath(bimm.cars))>0:
                #  print bimm.get_cars(main_page.xpath(bimm.cars)[0])
            if len(main_page.xpath(bimm.handle))>0:
                #print main_page.xpath(bimm.handle)[0].text_content()
                userdata.append(('Handle',main_page.xpath(bimm.handle)[0].text_content()))
                #if len(main_page.xpath(bimm.bio))>0:
                #  print main_page.xpath(bimm.bio)[0].text_content()
            if len(main_page.xpath(bimm.occupation))>0:
                #print main_page.xpath(bimm.occupation)[0].text_content()
                userdata.append(('Occupation',main_page.xpath(bimm.occupation)[0].text_content()))
            if len(main_page.xpath(bimm.ulink))>0:
                #print main_page.xpath(bimm.ulink)[0].text_content()
                userdata.append(('Link',main_page.xpath(bimm.ulink)[0].text_content()))
                #if len(main_page.xpath(bimm.name))>0:
                #  print bimm.get_name_email(main_page.xpath(bimm.name)[0])
                #print userdata
            if not debug:
                udb.insert_into_table(userdb, userdata)
                udb.close()
            else:
                print userdata
    else:
        pass
      
def e90post_thread_grab(url,postsdb = 'e90post_posts', debug = True):
        bimm = e90post()
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
                threaddata = []
                if t.xpath(bimm.posterid):
                    threaddata.append(('TimeOfPost',bimm.convert_to_valid_date(bimm.last_activity(t.xpath(bimm.timeofpost)[0].text_content().strip()))))
                    #print '**********************************************************************'
                    #print t.xpath(bimm.timeofpost)[0].text_content().strip()
                    
                    #print bimm.poster_id(t.xpath(bimm.posterid)[0])#[0].text_content()
                    threaddata.append(('PosterID',bimm.poster_id(t.xpath(bimm.posterid)[0])))
                    
                    #print bimm.post_id(t.xpath(bimm.postid)[0])#[0].text_content()
                    threaddata.append(('PostID',bimm.post_id(t.xpath(bimm.postid)[0])))
                    threaddata.append(('ThreadID',bimm.thread_id(t.xpath(bimm.post_thread)[0])))
                    try:
                        threaddata.append(('PostCountInThread',t.xpath(bimm.postcount)[0].text_content()))
                        #print t.xpath(bimm.postcount)[0].text_content()
                    except AttributeError:
                        #print t.xpath(bimm.postcount)[0]
                        threaddata.append(('PostCountInThread',t.xpath(bimm.postcount)[0]))
                    #print t.xpath(bimm.postlink)#[0].text_content()
                    #print '**********************************************************************'
                    threaddata.append(('Link',t.xpath(bimm.postlink)[0]))
                    e90post_user_grab(bimm.domain+t.xpath(bimm.posterid)[0], 'e90post_users')
                    if not debug:
                        udb.insert_into_table(postsdb, threaddata)
                    else:
                        print threaddata
            if next:
                #pdb.set_trace() 
                next_page = xmlTree(bimm.domain+next+alltime)
            elif not next:
                break
         
def e90post_grab(threaddb = 'e90post_threads', debug = True):
    bmw = e90post()
    main_page = xmlTree(bmw.domain)
    lvl1 = main_page.xpath(bmw.linklist)
    if not debug:
        udb = DBManager()
    for lvl1_link in lvl1:
        print lvl1_link
        next_page = xmlTree(bmw.domain+lvl1_link.attrib['href']+alltime)
        #next_page = xmlTree(lvl1_link)
        print bmw.domain+lvl1_link[0].text_content()
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
                if j.xpath(bmw.description):
                    threaddata = []
                    threaddata.append(('Description', j.xpath(bmw.description)[0].text_content().encode('utf-8')))
                    #print j.xpath(bmw.description)[0].text_content().encode('utf-8')
                    threaddata.append(('Replies', j.xpath(bmw.replies)[0].text_content()))
                    #print j.xpath(bmw.replies)[0].text_content()
                    threaddata.append(('Views', j.xpath(bmw.views)[0].text_content()))
                    #print j.xpath(bmw.views)[0].text_content()
                    threaddata.append(('Link', j.xpath(bmw.link)[0] ))
                    if not debug:
                        udb.insert_into_table(threaddb, threaddata)
                    else:
                        print threaddata
                    e90post_thread_grab(bmw.domain+j.xpath(bmw.link)[0])
                    #print j.xpath(bmw.link)[0]
            for k in threads:
                pass
                #                print k
            if next:
                next_page = xmlTree(bmw.domain+next+alltime)
            
            elif not next:
                break
    if not debug:
        udb.close()
e90post_u = 'http://www.e90post.com/forums/member.php?u=71259'
e90post_thrd = 'http://www.e90post.com/forums/showthread.php?t=66970'     
threads = Fields(thread_table_fields, 'threads')
posts = Fields(posts_table_fields, 'posts')
users = Fields(user_table_fields, 'users')       
if __name__=='__main__':
    #e90 = e90post()
    #e90post_thread_grab(e90post_thrd)
#    dbf = DBManager()
#    dbf.create_tables('e90post', 'users', users)
#    dbf.create_tables('e90post', 'threads', threads)
#    dbf.create_tables('e90post', 'posts', posts)
    #e90post_user_grab(e90post_u)
    e90post_thread_grab(e90post_thrd)
#    e90post_grab()