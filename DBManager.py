import types
import string

from time import sleep # time sleep pauses execution of script for the paramatere number of seconds
import codecs # this is for printing UTF-8 characters into a file standard python
import types # this is for comparing an item with types.NoneType standard python
import pyodbc # this is a library for database connection, it has interfaces for ms access, mysql, mssql, excel
#from sys import *
import sys # various system variables and functions available in the standard python library
import pdb
import lxml
from datetime import datetime
import time
import config
import re
from utils import *
class DBManager:
    
    def __init__(self, server = config.SERVER, port = config.PORT, db = config.DATABASE, user = config.USER, pwd = config.PASSWORD, chars = config.CHARSET, autoc = True):
        self.server = server
        self.port = port
        self.db = db
        self.user = user
        self.pwd = pwd
        self.chars = chars
        self.cnxn = pyodbc.connect('DRIVER={MySQL};SERVER=%s;DATABASE=%s;\
                                    CHARSET=UTF8;\
                                     SOCKET=/var/run/mysqld/mysqld.sock;UID=%s;PASSWORD=%s;OPTION=3;'\
                                     % (self.server, self.db, self.user, self.pwd))

    def create_table(self, name, fieldlist = []):
        creator = self.cnxn.cursor()
        loopy = 0
        query = "CREATE TABLE %s ("
        for t in fieldlist:
            query += t[0]+' '+t[1]
            loopy += 1
            if loopy < len(fieldlist):
                query +=', '
        query +=');'
        #print query % name
        #if not self.table_exists(name):
        try:
            creator.execute(query % name)
        except pyodbc.ProgrammingError:
            pass
        #self.cnxn.commit()
        creator.close()
    
    def user_exists(self, name, values):
        for m in values:
            if m[0]=='Handle':
                value = re.sub('\'','',m[1])
        locator = self.cnxn.cursor()
        query = "SELECT * FROM %s WHERE BINARY Handle=BINARY'%s';"
        #print query % (name,values)
        rows = 0
        try:
            rows = locator.execute(query % (name,value)).rowcount
        except UnboundLocalError:
            return False
#            print 'ceva'
#        except UnboundLocalError:
#            return False
#        except pyodbc.ProgrammingError:
#            print query % (name,value)
        if rows>0:
            locator.close()
            return True
        else:
            locator.close()
            return False
        
    def insert_into_table(self, name, fields = [], que = ""):
        if not self.user_exists(name, fields):
                    inserter = self.cnxn.cursor()
                    loopy = 0
                    query = "INSERT INTO %s ("
                    for t in fields:
                        if sanitize(t[1].strip()) != '':
                            query += t[0]
                            loopy += 1
                            if loopy < len(fields) and notvoid(fields[loopy]):
                                query += ', '
                            elif loopy < len(fields)-1:
                                query += ', '
                        else:
                            loopy += 1
                    query +=') VALUES ('
                    loopy = 0
                    for t in fields:
                        if sanitize(t[1].strip()) != '':
                            query += "\'"
                            query += re.sub('\'','',mysqlfriendly(t[1]))
                            query += "\'"
                            loopy += 1
                            if loopy < len(fields) and notvoid(fields[loopy]):
                                query += ', '
                            elif loopy < len(fields)-1:
                                query += ', '
                        else:
                            loopy += 1
                            
                    query += ');'
                    try:
                        inserter.execute(query % name)
                    except TypeError:
                        print query, name
                    #    pass
                    self.cnxn.commit()
                    inserter.close()
        else:
            pass
    def table_exists(self, name):
        query = """SELECT table_name
                   FROM information_schema.tables
                   WHERE table_schema = '%s'
                   AND table_name = '%s';
                   """
#        print query % (self.db,name)
        checker = self.cnxn.cursor()
        k=0
        for row in checker.tables():
            k+=1#.table_name)#.encode('ascii')#.encode('utf-8')
            #print unicode(name)
#            print k
            if row.table_name == name:
                return True
        else:
            return False
#        row = checker.fetchone().encode('utf-8')
#        if row:
#            checker.close()
#            return True
#        else:
#            checker.close()
#            return False

    def entry_exists(self, table_name, field_name, value):
        query = """
                    SELECT * FROM %s WHERE %s='%s';"""
        checker = self.cnxn.cursor()
        rows = checker.execute(query % (table_name, field_name, value))
        for row in rows:
            print "entry %s already exists in table" % row.anama
            checker.close()
            return True
        checker.close()
        return False 
    
    def close(self):
        self.cnxn.close()

    def create_tables(self, forum_name, data_type, fields = None):
        db_handler = DBManager()
        if not db_handler.table_exists(forum_name+'_'+data_type):
            if fields.__name__=='users':
                db_handler.create_table(forum_name+'_'+data_type, fields.fields )
            elif fields.__name__=='posts':
                db_handler.create_table(forum_name+'_'+data_type, fields.fields )
            elif fields.__name__=='threads':
                db_handler.create_table(forum_name+'_'+data_type, fields.fields )
        else:
            pass
        db_handler.close()

q = "INSERT INTO vwvortex_users (Location, Cars, Interests, TotalPosts,\
             LastActivity, JoinDate, Handle, Occupation) VALUES ('Massachusetts', '2002.5 VW Jetta 1.8T', 'Cars, dirtbikes, vagina',\
             ' 5726', '2011-02-09T01:27', '2002-03-17', 'White Jetta', 'Several');"
if __name__=='__main__':
    dday = '2011-01-22 05:39 PM'
    
    #print t
#    dby = DBManager()
    #dby.create_table('ascor', config.posts_table_fields)
#    print dby.user_exists('audiworld_users', [('Handle','escargot'),])
    dby.close()
    #dby.insert_into_table('vwvortex_users')
    
#    print dby.entry_exists('bolly', 'anama', 'first entry')


