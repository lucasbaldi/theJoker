# ****************************************
# Written By:
# 	stimalsina@connectedlab.com
# 	jhuschilt@connectedlab.com
#	lbaldi@connectedlab.com
#	jchung@connectlabb.com
#   sbalasuriya@connectedlab.com
#
# Created: 2016/05/09
# Revision History: version 1 - 2016/05/09
#					version 2 - 2016/05/31
# *****************************************

import ast
import json
import os
import time
import math
import thread
import signal
import random
import urllib
import token
from slackclient import SlackClient


# SCRIPT DEPENDENT VALUES: the following two variables must be set appropriately.
try:
	slackToken = token.privateSlackToken
except:
	errorMessage = "Cannot find slack Token !\n Please make sure there is a file named token.py with content similar to:\n"\
		"privateSlackToken = {your token}\n\n And import token in your script!"
	quit(errorMessage)

workingDirectory = "/Users/jenkins/Documents/JenkinsIOS/clqa-scripts/qualityBot"
chatbotID = "U0P44K8PM"

hourSeconds = 3600
pollIsStillOpen = True # poll timeout flag
replyCount = 0
responseThreshold = 2.0 / 3
userListFile="clUsers.txt"
responseOutputFile = "qualityWeeklyResponses.txt"

#responseThreshold = 2 / 3

#### Question Constants ####
greeting1="Hey wassup, I would like to ask you a really quick question:\nFrom 1 to 7, how would you say we are doing on <https://sites.google.com/a/connectedlab.com/starting/quality-assurance/quality-of-service-and-product|_*Quality of Product*_> this week? "
greeting2="Cool, cool.. one more question:\nCould you also let us know how you think we are doing (from 1 to 7) regarding <https://sites.google.com/a/connectedlab.com/starting/quality-assurance/quality-of-service-and-product|_*Quality of Service*_> this week?"
invalidResponse=["Sorry, but could you please just reply with a value from 1 to 7?", "I really just need an answer that is a number from 1 to 7...", "Are you trying to QA this survey or something?  Please, just a number from 1 to 7."]
numberTooBigResponse="_??!_  This number is too big.. please try again."
timeoutResponse1="Hey again. Did you get a chance to reply to my question yet?\nIt's been three hours..."
timeoutResponse2="Hey again! Now it's been a whole day! Please reply when you see this message."
'''
timeoutResponse3="It's been over three hours.. could you reply to my question please?"
timeoutResponse4="It's now four hours.. i'm still waiting... waiting..\n...and waiting.."
timeoutResponse5="Hey.. me again.  You haven't checked Slack all day.  Please reply to the survey as soon as you get a chance"
timeoutResponse6="Sup. Please take a second to quickly reply to this survey.  It will only be open for a few more hours."
'''
closer1="Ok, cool.  Thanks very much!"
closer2="Your feedback will be reflected anonymously on the dashboard very soon."
closedPoll="\n---------------- Survey Closed ----------------\nThe survey poll for this week is now closed. If you missed it despite the reminders, there will be another one next week.\n\nThanks very much,\n- Connected B0T"

pollStartTime = time.time()
print "\n--- New Survey: %s : %d ---" % (time.strftime("%Y/%m/%d"), pollStartTime)

listOfUsers = "%s/%s" % (workingDirectory, userListFile)	# prod use clUsers.txt | test
#listOfUsers = "%s/clUsersTest.txt" % workingDirectory		# prod use clUsers.txt | test use clUsersTest.txt
outPutResponses = "%s/%s" % (workingDirectory, responseOutputFile)
slackClientObject = SlackClient(slackToken)


def closePoll():
	global pollIsStillOpen
	global responseList
	signal.alarm(0)
	print("Closing the Poll!")

	sendMsg("all", closedPoll)
	pollIsStillOpen = False # main method while flag

	# Write the results to file
	responseDataFile = open(outPutResponses, 'a+')
	for userEntry in responseList.keys():
		if (responseList[userEntry]['resp1'] != ''): # usrs answered 1 or more questions
			print >> responseDataFile, time.strftime("%Y/%m/%d") + " " + userEntry  + " " + str(responseList[userEntry]['resp1']) + " " + str(responseList[userEntry]['resp2'])
	responseDataFile.close()


def sendReminder(userID, remindersSent):
	print("reminder called! [%s]" % (time.strftime("%M/%s")))

	if (remindersSent < 0 and remindersSent > 1):
		return remindersSent

	switcher = {
		0: timeoutResponse1,
		1: timeoutResponse2,
		#2: timeoutResponse3,
		#3: timeoutResponse4,
		#4: timeoutResponse5,
		#5: timeoutResponse6,
	}

	response = switcher.get(remindersSent)

	#send reminder if user hasn't given both the responses
	if (responseList[userID]['resp2'] == ''):
		sendMsg(userID, response)


def sendMsg (userID, msg):
	global responseList
	if (userID == "all"):
		for currentUserID in responseList.keys():
			openChannelResponse = slackClientObject.api_call("im.open", user=currentUserID)
			chan = openChannelResponse['channel']['id']
			slackClientObject.api_call("chat.postMessage", as_user="true:", channel=chan, text=msg)
	else:
		openChannelResponse = slackClientObject.api_call("im.open", user=userID)
		chan = openChannelResponse['channel']['id']
		slackClientObject.api_call("chat.postMessage", as_user="true:", channel=chan, text=msg)


def populateInput(userID, inputText):
	global responseList
	global replyCount

	if (responseList[userID]['resp1'] == ''):
		responseList[userID]['resp1'] = int(inputText)
		sendMsg(userID, greeting2)
	elif(responseList[userID]['resp2'] == ''):
		responseList[userID]['resp2'] = int(inputText)
		sendMsg(userID, closer1)
		sendMsg(userID, closer2)
		replyCount += 1
	else:
		print("user completed survey!")


def isValidInput(userID, inputText):
	global responseList

	#send reminder if user hasn't given both the responses
	if (responseList[userID]['resp2'] != ''):
		return False

	if (not inputText.isdigit()):
		sendMsg(userID, invalidResponse[random.randint(0,2)])
		return False

	elif (int(inputText) < 1):

		sendMsg(userID, invalidResponse[random.randint(0,2)])
	 	return False

	elif (int(inputText) > 7):
		sendMsg(userID, numberTooBigResponse)
	 	return False

	return True

numberOfReminders = 0
def callReminder(sig, stack):
	global numberOfReminders
	global responseList
	print ("Call reminder")

	# Remind each user
	for userEntry in responseList.keys():
		sendReminder(userEntry, numberOfReminders)

	if(numberOfReminders < 1):
		signal.alarm(24*hourSeconds) # Next Day (Saturday)
	elif(numberOfReminders == 1):
		signal.alarm(24*hourSeconds) # Next Day (Sunday)
	else:
		closePoll()

	'''
	elif(numberOfReminders == 5):
		signal.alarm(19*hourSeconds) # 43 hours
	elif(numberOfReminders == 6):
		signal.alarm(5*hourSeconds) # 48 hours
	'''

	numberOfReminders += 1

# Main Method
responseList = {}  # a dictionary of dictionaries
with open(listOfUsers, "rw+") as userIDFile:
	for lines in userIDFile:
		currentUser = lines.rstrip('\n')
		sendMsg(currentUser, greeting1)
		responseList[str(currentUser)] = { 'resp1':'' , 'resp2': ''}

numberOfUsers = len(responseList)
print(responseList)

if slackClientObject.rtm_connect():
	signal.signal(signal.SIGALRM, callReminder)
	signal.alarm(3*hourSeconds)  #Three hours after (~1pm Friday)

	while pollIsStillOpen:
		new_evts = slackClientObject.rtm_read()

		for event in new_evts:
			#print event
			if "user" in event and event["user"] == chatbotID:
				continue

			if "type" in event:
				if event["type"] == "message" and "text" in event:
					# print(urllib.quote(event["text"]))
					print(event["text"].encode('utf-16'))

					if (len(event['text']) > 1):
						sendMsg(event["user"], invalidResponse[random.randint(0,2)])
						continue

					if (isValidInput(event['user'], event['text'])):
						populateInput(event["user"], event["text"])

					print(responseList)

		if replyCount >= math.ceil(numberOfUsers * responseThreshold):
			closePoll()
			pollIsStillOpen = False
else:
	print ("Connection Failed, Invalid Token")
os.system("aws s3 cp " + responseOutputFile + " s3://connected-project-status/slackResults/ --acl public-read")
