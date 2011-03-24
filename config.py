'''
Created on Feb 2, 2011

@author: arturd
'''

SERVER = 'localhost'
USER = 'root'
PASSWORD = 'welcome'
SOCKET = ''
DATABASE = 'mynewstuff'
PORT = '3306'
CHARSET = 'UTF8'
SOCKET = ''
user_table_fields = [('Location','varchar(200)'), ('Name','varchar(20)'), ('Cars','text'),('Handle','varchar(50)'),\
                       ('Interests','text'),('TotalPosts','int'),('LastActivity','datetime'),('JoinDate','date'),\
                       ('PositiveFeedback','int(3)'),('NegativeFeedback','int(3)'),('PostsPerDay', 'float'),\
                       ('Biography','text'),('Occupation','varchar(200)'),('Link','varchar(200)'),('PosterID','varchar(50)')]
                       
posts_table_fields = [('PostID','int'),('ThreadID','int'),('PosterID','varchar(50)'),('TimeOfPost','datetime'),\
                      ('PostCountInThread','int(3)'),('Link','varchar(200)')]

thread_table_fields = [('Description','varchar(50)'),('Link','varchar(200)'),('ThreadID','varchar(10)'),('Replies','int(7)'),\
                       ('Views','int(7)')]
