'''
Created on Jan 25, 2011

@author: arturd
'''
from utils import *
from DBManager import DBManager
from vwvortex import vwvortex
from config import *
def vwvortex_user_grab(url,userdb = 'vwvortex_users', debug = True):
    bimm = vwvortex()
    main_page = xmlTree(url)
    userdata = []
    if main_page:
            if not debug:
                udb = DBManager()
                #pdb.set_trace()
            if len(main_page.xpath(bimm.location))>0:
                #print main_page.xpath(bimm.location)[0].text_content().strip()
                userdata.append(('Location',main_page.xpath(bimm.location)[0].text_content().strip()))
            if len(main_page.xpath(bimm.cars))>0:
                #print main_page.xpath(bimm.cars)[0].text_content()
                userdata.append(('Cars',main_page.xpath(bimm.cars)[0].text_content()))
            if len(main_page.xpath(bimm.interests))>0:
                #print main_page.xpath(bimm.interests)[0].text_content()
                userdata.append(('Interests', main_page.xpath(bimm.interests)[0].text_content()))
            if len(main_page.xpath(bimm.noposts))>0:
                #print bimm.total_posts(main_page.xpath(bimm.noposts)[0].text_content())
                userdata.append(('TotalPosts', bimm.total_posts(main_page.xpath(bimm.noposts)[0].text_content())))
            if len(main_page.xpath(bimm.lastac))>0:
                #print bimm.last_activity(main_page.xpath(bimm.lastac)[0].text_content())
                userdata.append(('LastActivity', bimm.convert_to_valid_date(bimm.last_activity(main_page.xpath(bimm.lastac)[0].text_content()))))
            if len(main_page.xpath(bimm.joindate))>0:
                #print bimm.join_date(main_page.xpath(bimm.joindate)[0].text_content())
                userdata.append(('JoinDate', bimm.convert_to_valid_date(bimm.join_date(main_page.xpath(bimm.joindate)[0].text_content()))))
                #if len(main_page.xpath(bimm.ppday))>0:
                #  print bimm.p_p_day(main_page.xpath(bimm.ppday)[0].text_content())
                #if len(main_page.xpath(bimm.cars))>0:
                #  print main_page.xpath(bimm.cars)[0].text_content()
            if len(main_page.xpath(bimm.handle))>0:
                #print bimm.get_handle(main_page.xpath(bimm.handle)[0].text_content())
                userdata.append(('Handle', bimm.get_handle(main_page.xpath(bimm.handle)[0])))
                #if len(main_page.xpath(bimm.bio))>0:
                #  print main_page.xpath(bimm.bio)[0].text_content()
            if len(main_page.xpath(bimm.occupation))>0:
                #print main_page.xpath(bimm.occupation)[0].text_content()
                userdata.append(('Occupation', main_page.xpath(bimm.occupation)[0].text_content()))
            if len(main_page.xpath(bimm.ulink))>0:
                userdata.append(('Link',main_page.xpath(bimm.ulink)[0].text_content()))
                # print main_page.xpath(bimm.ulink)[0].text_content()
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
def vwvortex_thread_grab(url,postsdb = 'vwvortex_posts', debug = False):
    bimm = vwvortex()
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
            threaddata = []
            if t.xpath(bimm.posterid):
                threaddata.append(('TimeOfPost',bimm.convert_to_valid_date(bimm.last_activity(t.xpath(bimm.timeofpost)[0]\
                                                                                              .text_content().strip()))))
                #print t.xpath(bimm.timeofpost)[0].text_content().strip()
                threaddata.append(('PosterID',bimm.poster_id(t.xpath(bimm.posterid)[0])))
                #print bimm.poster_id(t.xpath(bimm.posterid)[0])#[0].text_content()
                threaddata.append(('PostID',bimm.post_id(t.xpath(bimm.postid)[0])))
                #print bimm.post_id(t.xpath(bimm.postid)[0])#[0].text_content()
                try:
                    threaddata.append(('PostCountInThread', t.xpath(bimm.postcount)[0].text_content().strip('#')))
                    #print t.xpath(bimm.postcount)[0].text_content()
                except AttributeError:
                    threaddata.append(('PostCountInThread', t.xpath(bimm.postcount)[0].strip('#')))
                    #print t.xpath(bimm.postcount)[0]
                except IndexError:
                    pass
                threaddata.append(('ThreadID',bimm.thread_ID(t.xpath(bimm.postlink)[0])))
                threaddata.append(('Link',t.xpath(bimm.postlink)[0]))
                #print t.xpath(bimm.postlink)#[0].text_content()
                vwvortex_user_grab(bimm.domain+t.xpath(bimm.posterid)[0],'vwvortex_users')
                if not debug:
                    udb.insert_into_table(postsdb, threaddata)
                else:
                    print threaddata
        if next:
            #pdb.set_trace() 
            next_page = xmlTree(bimm.domain+next+alltime)
        elif not next:
            if not debug:
                udb.close()
            break



def vwvortex_grab(threaddb = 'vwvortex_threads', debug = True):
    #      pdb.set_trace()
    bmw = vwvortex()
    main_page = xmlTree(bmw.domain)
    lvl1 = main_page.xpath(bmw.linklist_lvl1)
    if not debug:
        udb = DBManager()
    for lvl1_link in lvl1:
        second_lvl_page = xmlTree(bmw.domain+lvl1_link)
        lvl2 = second_lvl_page.xpath(bmw.linklist_lvl2)
        for lvl2_link in lvl2:
            next_page = xmlTree(bmw.domain+lvl2_link+alltime)
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
                        threaddata.append(('Views', bmw.parse_views(j.xpath(bmw.views)[0].text_content())['Views']))
                        #print bmw.parse_views(j.xpath(bmw.views)[0].text_content())
                        threaddata.append(('Link', j.xpath(bmw.link)[0].encode('utf-8')))
                        #print j.xpath(bmw.link)[0].encode('utf-8')
                        #print bmw.thread_id(j.xpath(bmw.link)[0].encode('utf-8'))
                        
                        vwvortex_thread_grab(bmw.domain+j.xpath(bmw.link)[0].encode('utf-8'))
                        if not debug:
                            udb.insert_into_table(threaddb, threaddata)
                        else:
                            print threaddata
                        #vwvortex_thread_grab()
#            for k in threads:
#                pass
                #                print k
                    if next:
                        next_page = xmlTree(bmw.domain+next)
            
                    elif not next:
                        break
    if not debug:
        udb.close()
vwvortex_thrd = 'http://forums.vwvortex.com/showthread.php?5073084-The-Official-FML-Thread'
anthr_thrd = 'http://forums.vwvortex.com/showthread.php?5212980-Will-Subaru-discontinue-the-STI/page2&s=ec0d99c07427a800711ab0fd7a4be702'
vwvortex_u = 'http://forums.vwvortex.com/member.php?475874'
threads = Fields(thread_table_fields, 'threads')
posts = Fields(posts_table_fields, 'posts')
users = Fields(user_table_fields, 'users')
if __name__=='__main__':
    #vw = vwvortex()
    
#    vwvortex_user_grab(vwvortex_u, debug = True)
#    dbf = DBManager()
#    dbf.create_tables('vwvortex', 'users', users)
#    dbf.create_tables('vwvortex', 'threads', threads)
#    dbf.create_tables('vwvortex', 'posts', posts)
    vwvortex_thread_grab(anthr_thrd,debug=True)
#    vwvortex_grab(debug=False)