# -*- coding: utf-8 -*-s
"""
Created on Fri Feb 14 13:05:41 2020

@author: User
#cursor.execute("DROP TABLE Candidate")
#cursor.execute("DROP TABLE Recruiter")
#cursor.execute("DROP TABLE CandidateDetails")
#cursor.execute("DROP TABLE JobPostings")
#conn.execute("CREATE TABLE Candidate (USER_NAME TEXT NOT NULL,EMAIL TEXT NOT NULL PRIMARY KEY,PASSWORD CHAR(20) NOT NULL);")
#c.execute("CREATE TABLE Recruiter (COMPANY_NAME TEXT NOT NULL,EMAIL TEXT NOT NULL PRIMARY KEY, PASSWORD CHAR(20) NOT NULL)")


"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:11:59 2020

@author: ELCOT
"""

'''
un="dhakshin@gmail.com"

sql_update_query = """DELETE from CandidateDetails where username = ?"""
c.execute(sql_update_query, (un, ))
conn.commit()

un=""

sql_update_query = """DELETE from CandidateDetails where username = ?"""
c.execute(sql_update_query, (un, ))
conn.commit()

#c.execute("CREATE TABLE CandidateDetails (username varchar(30) PRIMARY KEY, data json NOT NULL)")
#c.execute("CREATE TABLE JobPostings (COMPANY TEXT NOT NULL,LOCATION TEXT NOT NULL,SKILL json NOT NULL,DESIGNATION TEXT NOT NULL,EXPERIENCE TEXT NOT NULL,EDUCATION TEXT NOT NULL)")

'''



import sqlite3;
conn = sqlite3.connect('project.db')
cursor = conn.cursor()

print("\n\nCandidate db content")
conn.commit()
for row in conn.execute('select * from candidate'): 
    print(row)
    print()
conn.close()

print("---------------------------------------------------------------------------")


import sqlite3
conn = sqlite3.connect('project.db')
c=conn.cursor()
print("\n\n\nRecruiter db content")
for row in conn.execute('select * from Recruiter'): 
    print(row)
    print()
conn.close()

print("---------------------------------------------------------------------------")

        
import sqlite3
conn = sqlite3.connect('project.db')
c=conn.cursor()
conn.commit()
print("\n\n\nCandidate Details db content")
for row in conn.execute('select * from CandidateDetails'): 
    print(row)
    print()
conn.close()

print("---------------------------------------------------------------------------")

import sqlite3
conn = sqlite3.connect('project.db')
c=conn.cursor()
conn.commit()
print("\n\n\nJob posting db content")
for row in conn.execute('select * from JobPostings'): 
    print(row)
    print()
conn.close()

