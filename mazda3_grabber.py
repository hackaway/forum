from utils import *
from DBManager import DBManager
from mazda3 import mazda3
from config import *
def mazda3_user_grab(url, userdb = 'mazda3_users',debug = True):
    bimm = mazda3()
    main_page = xmlTree_w_login(url, 'mazda', 'somebodyis', 'anybodyanybody')
    userdata = []
    if main_page:
            if not debug:
                udb = DBManager()
            #pdb.set_trace()
            if len(main_page.xpath(bimm.location))>0:
                #print main_page.xpath(bimm.location)[0].text_content().strip()
                userdata.append(('Location', main_page.xpath(bimm.location)[0].text_content().strip()))
            if len(main_page.xpath(bimm.car_make))>0:
                #print main_page.xpath(bimm.cars)[0].text_content()
                userdata.append(('Cars', main_page.xpath(bimm.car_make)[0].text_content()\
                                   +main_page.xpath(bimm.car_year)[0].text_content()))
        #   if len(main_page.xpath(bimm.interests))>0:
        #       #print main_page.xpath(bimm.interests)[0].text_content()
        #       userdata.append(('Interests', main_page.xpath(bimm.interests)[0].text_content()))
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
            if len(main_page.xpath(bimm.minus_fb))>0:
                userdata.append(('NegativeFeedback', main_page.xpath(bimm.minus_fb)[0].text_content().strip()))
            if len(main_page.xpath(bimm.plus_fb))>0:
                userdata.append(('PositiveFeedback', main_page.xpath(bimm.plus_fb)[0].text_content().strip()))
            if not debug:
                udb.insert_into_table(userdb, userdata)
                udb.close()
            else:
                print userdata
    else:
        pass

def mazda3_thread_grab(url, postsdb = 'mazda3_posts', debug = True):
        bimm = mazda3()
        next_page = xmlTree(url)
        lvl1 = next_page.xpath(bimm.postdata)
        count = 0
        pos = url.find('topic=') + len('topic=')
        part = url[:pos]
        fid = url[pos:]
        ifid = fid.split(r'.')
        if not debug:
            udb = DBManager()
        try:
            lastpage = int(next_page.xpath(bimm.last_page_threads)[0].text_content())
        except IndexError:
                lastpage = 1 
        
        while count<lastpage:
                posts = next_page.xpath(bimm.postdata)
                for pst in posts:
                        threaddata = []
                        threaddata.append(('TimeOfPost',bimm.convert_to_valid_date(bimm.last_activity(bimm.time_of_post(pst.xpath(\
                                                                    bimm.timeofpost)[0].text_content())))))
                        #print bimm.time_of_post(pst.xpath(bimm.timeofpost)[0].text_content())
                        threaddata.append(('PosterID',bimm.poster_id(pst.xpath(bimm.posterid)[0])))
                        #print pst.xpath(bimm.posterid)[0]
                        threaddata.append(('PostID',bimm.post_id(pst.xpath(bimm.postid)[0])))
                        #print pst.xpath(bimm.postid)[0]
                        threaddata.append(('Link',pst.xpath(bimm.postlink)[0]))
                        #print pst.xpath(bimm.postlink)[0]
                        threaddata.append(('PostCountInThread',bimm.post_count(pst.xpath(bimm.postcount)[0].text_content())))
                        threaddata.append(('ThreadID', bimm.thread_id(pst.xpath(bimm.post_thread)[0])))
                        #print bimm.post_count(pst.xpath(bimm.postcount)[0].text_content())
                        mazda3_user_grab(pst.xpath(bimm.posterid)[0],'mazda3_users')
                        if not debug:
                            udb.insert_into_table(postsdb, threaddata)
                        else:
                            print threaddata
                count += 1
                #print count
                #print part+addto(ifid,count)
                next_page = xmlTree(part+addto(ifid,count))
        if not debug:
            udb.close()
            
            
def mazda3_grab(threaddb = 'mazda3_threadas', debug =True):
    #pdb.set_trace()
    bmw = mazda3()
    main_page = xmlTree(bmw.domain)
    lvl1 = main_page.xpath(bmw.linklist)
    if not debug:
        udb = DBManager()
    for lvl1_link in lvl1:
        next_page = xmlTree(lvl1_link)
        count = 0
        pos = lvl1_link.find('board=') + len('board=')
        part = lvl1_link[:pos]
        fid = lvl1_link[pos:]
        ifid = fid.split(r'.')
    
        try:
            lastpage = int(next_page.xpath(bmw.last_page_threads)[0].text_content())
        except IndexError:
            lastpage = 1
        while count<lastpage:
      
            #threads_list = next_page.xpath(bmw.threaddata)
            threads = next_page.xpath(bmw.threads_list)
            tread_data = next_page.xpath(bmw.threaddata)
            for j in tread_data:
                #pass
                threaddata = []
                if j.xpath(bmw.description):
                    threaddata.append(('Description',j.xpath(bmw.description)[0].text_content().encode('utf-8')))
                    #print j.xpath(bmw.description)[0].text_content().encode('utf-8')
                    threaddata.append(('Views', bmw.parse_stats(j.xpath(bmw.stats)[0].text_content())['Views']))
                    threaddata.append(('Views', bmw.parse_stats(j.xpath(bmw.stats)[0].text_content())['Replies']))
#                    print bmw.parse_stats(j.xpath(bmw.stats)[0].text_content())
                    #print j.xpath(bmw.views)[0].text_content()
                    threaddata.append(('Link', j.xpath(bmw.link)[0]))
#                    print j.xpath(bmw.link)[0]
                    mazda3_thread_grab(bmw.thread_id(j.xpath(bmw.link)[0]))
                if not debug:
                    udb.insert_into_table(threaddb, threaddata)
                    #pass
                else:
                    print threaddata
            count += 1
            print count
            print part+addto(ifid,count)
            next_page = xmlTree(part+addto(ifid,count))
    if not debug:
        udb.close()
mazda3_u = 'http://www.mazda3forums.com/index.php?action=profile;u=53648'
mazda3_thrd = 'http://www.mazda3forums.com/index.php?topic=153225.0'      
threads = Fields(thread_table_fields, 'threads')
posts = Fields(posts_table_fields, 'posts')
users = Fields(user_table_fields, 'users')
if __name__=='__main__':
    #mz = mazda3()   
    #mazda3_thread_grab(mazda3_thrd) 
    #mazda3_grab()
#    dbf = DBManager()
#    dbf.create_tables('mazda3', 'users', users)
#    dbf.create_tables('mazda3', 'threads', threads)
#    dbf.create_tables('mazda3', 'posts', posts)
    #mazda3_user_grab(mazda3_u)
    mazda3_thread_grab(mazda3_thrd) 
    #mazda3_grab()