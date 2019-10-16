import sys,os,json,re,random

f = open('dataset/train.json')
dtrain = json.loads(f.read())
f.close()

lines = []

random.seed(99)

import csv
 
header = ['question1', 'question2', 'is_duplicate']

for idx,item in enumerate(dtrain):
    nnqt = item['NNQT_question']
    question = item['question']
    tokens = re.findall('\{.*?\}',nnqt)
    cleantokens = [re.sub('\W+',' ', token) for token in tokens]
    _tokensentence = ' '.join(cleantokens)
    tokensentence = re.sub(' +', ' ', _tokensentence)
    #perfect sentence pair
    lines.append([tokensentence,question,1.0])
    #print((tokensentence,question,1))
    #less than perfect pairs
    s = ''
    for idx,chunk in enumerate(cleantokens):
        s += chunk
        lines.append([re.sub(' +', ' ', s),question,(idx+1)*1.0/float(len(cleantokens))])
        #lines.append((re.sub(' +', ' ', s),question,0))
        #print((re.sub(' +', ' ', s),question,(idx+1)*1.0/float(len(cleantokens))))
    #0 match pair
    randidx = random.randint(0,len(dtrain)-1)
    randnnqt = dtrain[randidx]['NNQT_question']
    randtokens = re.findall('\{.*?\}', randnnqt)
    if len(set(tokens) - (set(tokens) - set(randtokens))) == 0:
        cleanrandtokens = [re.sub('\W+',' ', token) for token in randtokens]
        _randtokensentence = ' '.join(cleanrandtokens)
        randtokensentence = re.sub(' +', ' ', _randtokensentence)
        lines.append([randtokensentence,question,0.0])
        #print((randtokensentence,question,0.0))

with open('lcq2train1.csv', 'wt') as f:
    csv_writer = csv.writer(f,quoting=csv.QUOTE_ALL)
 
    csv_writer.writerow(header) # write header
 
    for line in lines:
        csv_writer.writerow(line)
f.close()
