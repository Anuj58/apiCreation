__author__ = "Anuj Chaturvedi"
__date__ = "Sep, 2015"

application_port = 2212

import time

print "Starting All Loads:", time.time()

import os
import web
import sys

import datetime

LogDir="/data/analytics/APILogs/LeadScoringLogs"

#Add project path to system path.
path = os.path.abspath(__file__)
source_code_folder = os.path.dirname(path)


sys.path.append(source_code_folder)

import datetime
from datetime import date
import simplejson
import urllib2
from pprint import pprint
import traceback
import AppMainFunctions

urls = ('/leadscore','leadscore','/alive','alive')


print_queries = True
print_responses = False

import csv


class alive:
   def GET(self):
       return "true"

class leadscore:
    def logToFile(self, users,LeadScore,LeadScoreNew, jsondata,time_taken):
        datestr=str(date.today())
        logFileName=LogDir+ '/LSlog_'+str(application_port)+ '_' + datestr+'.txt'
        f = open(logFileName, 'a')
        writer = csv.writer(f, delimiter = '|')
        cur_time = str(datetime.datetime.now())
        username = jsondata['username']
        row = [cur_time,users, username, str(LeadScore),LeadScoreNew,time_taken]
        #Logging Fields:"Timestamp","username","leadscore"
        writer.writerow(row)
        f.close()

    def POST(self):
        #This handles both search and job order based status candidate queries.
        #print "inside Post"
        start_time = time.time()
        query = web.data()
        try:
            jsondata = simplejson.loads(query)
            if print_queries:
                pprint(jsondata)
            username=jsondata['username']
            #print "Lead Score for the username =",username
            [users,LeadScore,LeadScoreNew] = AppMainFunctions.getLeadScore(username)
            print users,LeadScore,LeadScoreNew
            if print_responses:
                pprint(LeadScoreNew)
            #print "Time Taken to give response", time.time() - start_time, "seconds."
            time_taken=time.time() - start_time
            #Log to file
            self.logToFile(users,LeadScore,LeadScoreNew, jsondata,time_taken)
            return LeadScoreNew

        except:
            #writer.writerow(['Exception', traceback.format_exc()])
            traceback.print_exc()
            pass



#This is the code for running it under default web.py server.
if __name__ == "__main__":
    app = web.application(urls, globals())
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", application_port))
