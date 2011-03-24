'''
Created on Jan 25, 2011

@author: arturd
'''
from utils import *
from DBManager import DBManager
from priuschat import priuschat
from config import *
def priuschat_user_grab(url, userdb='priuschat_users', debug = False):
    bimm = priuschat() 
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
                userdata.append(('JoinDate', bimm.convert_to_valid_date(bimm.join_date(main_page.xpath(bimm.joindate)[0].text_content()))))
            if len(main_page.xpath(bimm.ppday))>0:
                #print bimm.p_p_day(main_page.xpath(bimm.ppday)[0].text_content())
                userdata.append(('PostsPerDay', bimm.p_p_day(main_page.xpath(bimm.ppday)[0].text_content())))
                  
            if len(main_page.xpath(bimm.cars))>0:
                #print main_page.xpath(bimm.cars)[0].text_content()
                userdata.append(('Cars',main_page.xpath(bimm.cars)[0].text_content()))
                  
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
                userdata.append(('Link', main_page.xpath(bimm.ulink)[0].text_content()))
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
          
def priuschat_thread_grab(url, postsdb = 'priuschat_posts',debug = False):
    bimm = priuschat()
    next_page = xmlTree(url)
    #posts = main_page
    if not debug:
        udb = DBManager()
    while True:
        try:
          
          next = next_page.xpath(bimm.next_link)[0]
          print next
                
        except IndexError:
            next = None
        posts = next_page.xpath(bimm.postdata)
        for t in posts:
            if t.xpath(bimm.posterid):
                threaddata = []
                threaddata.append(('TimeOfPost',bimm.convert_to_valid_date(bimm.last_activity(t.xpath(bimm.timeofpost)[0]\
                                                                                              .text_content().strip()))))
                #print t.xpath(bimm.timeofpost)[0].text_content().strip()
                threaddata.append(('PosterID',bimm.poster_id(t.xpath(bimm.posterid)[0])))
                #print bimm.poster_id(t.xpath(bimm.posterid)[0])#[0].text_content()
                threaddata.append(('PostID',bimm.post_id(t.xpath(bimm.postid)[0])))
                #print bimm.post_id(t.xpath(bimm.postid)[0])#[0].text_content()
                try:
                    threaddata.append(('PostCountInThread',t.xpath(bimm.postcount)[0].text_content()))
                    #print t.xpath(bimm.postcount)[0].text_content()
                except AttributeError:
                    threaddata.append(('PostCountInThread',t.xpath(bimm.postcount)[0]))
                    #print t.xpath(bimm.postcount)[0]
                threaddata.append(('Link',t.xpath(bimm.postlink)[0]))
                #print t.xpath(bimm.postlink)#[0].text_content()
                priuschat_user_grab(t.xpath(bimm.posterid)[0],'priuschat_users')
                if not debug:
                    udb.insert_into_table(postsdb, threaddata)
                else:
                    print threaddata
        if next:
                #pdb.set_trace() 
            next_page = xmlTree(next)
            
        elif not next:
            if not debug:
                udb.close()
            break
       
def priuschat_grab(threaddb = 'priuschat_threads', debug = True):
    bmw = priuschat()
    main_page = xmlTree(bmw.domain)
    lvl1 = main_page.xpath(bmw.linklist)
    if not debug:
        udb = DBManager()
    for lvl1_link in lvl1:
        print lvl1_link#.text_content()
        #next_page = xmlTree(bmw.domain+lvl1_link+alltime)
        next_page = xmlTree(lvl1_link+allmosttime)
        print bmw.domain+lvl1_link#.text_content()
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
                    threaddata.append(('Link', j.xpath(bmw.link)[0]))
                    #print j.xpath(bmw.link)[0]
                    #print bmw.thread_id(j.xpath(bmw.link)[0])
                    if not debug:
                        udb.insert_into_table(threaddb, threaddata)
                    else:
                        print threaddata
                    priuschat_thread_grab(j.xpath(bmw.link)[0])
            for k in threads:
                pass
                #                print k
            if next:
                next_page = xmlTree(next+allmosttime)
            
            elif not next:
                break
    if not debug:
        udb.close()
priuschat_u = 'http://priuschat.com/forums/members/dva.html'
priuschat_thrd = 'http://priuschat.com/forums/prius-hybrid-news/88002-prius-v-wagon-puzzle-finally-complete-heres-what-we-know.html'  
threads = Fields(thread_table_fields, 'threads')
posts = Fields(posts_table_fields, 'posts')
users = Fields(user_table_fields, 'users')          
if __name__=='__main__':
    #prius = priuschat()
    #priuschat_thread_grab(priuschat_thrd)
    dbf = DBManager()
    dbf.create_tables('priuschat', 'users', users)
    dbf.create_tables('priuschat', 'threads', threads)
    dbf.create_tables('priuschat', 'posts', posts)
    #priuschat_user_grab(priuschat_u)
    priuschat_thread_grab(priuschat_thrd)
    #priuschat_grab(debug=False)