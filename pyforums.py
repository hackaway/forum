from mechanize import Browser
import lxml
from lxml import html
import pyodbc
import codecs
#from config import *
import pdb
from bimmerfest_grabber import *
from audiworld_grabber import *
from feoa_grabber import *
from e90post_grabber import *
from mazda3_grabber import *
from namotoring_grabber import *
from vwvortex_grabber import *
from priuschat_grabber import *
import re
import time
from utils import Fields

user_table_fields = [('Location','varchar(30)'), ('Name','varchar(20)'), ('Cars','text'),('Handle','varchar(10)'),\
                       ('Interests','text'),('TotalPosts','int'),('LastActivity','datetime'),('JoinDate','date'),\
                       ('PositiveFeedback','int(3)'),('NegativeFeedback','int(3)'),('PostsPerDay', 'float'),\
                       ('Biography','text'),('Occupation','varchar(30)'),('Link','varchar(100)'),('PosterID','int')]
                       
posts_table_fields = [('PostID','int'),('ThreadID','int'),('PosterID','int'),('TimeOfPost','datetime'),\
                      ('PostCountInThread','int(3)'),('Link','varchar(100)')]

thread_table_fields = [('Description','varchar(50)'),('Link','varchar(100)'),('ThreadID','varchar(10)'),('Replies','int(7)'),\
                       ('Views','int(7)')]

threads = Fields(thread_table_fields, 'threads')
posts = Fields(posts_table_fields, 'posts')
users = Fields(user_table_fields, 'users')

from DBManager import DBManager


#user = 'somebodyis'
#pwd = 'anybodyanybody'
#fort = 'mazda'
#alltime = '&daysprune=-1'
#allmosttime = '?daysprune=-1'
#sticky = ".//td[contains(@id,'td_threadtitle')]/div/text()"




                
conection = []
      
      
        #threads = next_page.xpath(bmw.threads_list)








#user_list = [bimmer_user,audiworld_u,e90post_u, priuschat_u, feoa_u, mazda3_u, vwvortex_u]











if __name__=="__main__":
    dbf = DBManager()
    dbf.create_tables('audiworld', 'users', users)
    dbf.create_tables('audiworld', 'threads', threads)
    dbf.create_tables('audiworld', 'posts', posts)
    #bimmerfest_thread_grab(bimmerg)
#    for t in range(200):
#        bimmerfest_user_grab(bimmer_user)
    #bimmerfest_user_grab(bimmer_user)
    #e90post_user_grab(e90post_u)
    #priuschat_user_grab(priuschat_u)
    #mazda3_user_grab(user_list[5])
    #bimmerfest_thread_grab(bimmerfest_thrd)