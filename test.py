import json
import csv
import pandas as pd  
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
def test(data):
  result=[]
  for faq in data['data']:
    print(faq['ques'])
  #automating the testing 
  for faq in data['data']:
      fdata=json.dumps({"text":faq["ques"],"message_id": "b28"})
      response=requests.post(url="http://localhost:5005/model/parse",data=fdata)
      #print(response)
      response_list=json.loads(response.text)
      #print(response_list)
      result.append({"ans":faq["ans"],"bot_ans":response_list})
  return result

  
#loading data for testing
f = open('faqdata.json',encoding="utf8")
jsondata = json.load(f)
result=[]
result=test(jsondata)
#print(res)
ques=[]
ans=[]
confidence_scores=[]
qno=[]
confidence=[]
#Below code is to convert the data in result in to csv for better understanding
for i in result:
  ques.append(i['bot_ans']['text'])
  ans.append(i['ans'])
  confidence_scores.append(i['bot_ans']['intent_ranking'][0:3])
  qno.append(i['bot_ans']['intent']['name'])
  confidence.append(i['bot_ans']['intent']['confidence'])
dict = {'question': ques,'question label':qno,'confidence':confidence,'answer':ans,'Top 3 confidence scores':confidence_scores}
df = pd.DataFrame(dict)
#storing data into csv file
df.to_csv('data_file.csv')