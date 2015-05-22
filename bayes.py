# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re , operator, nltk
from nltk.stem import PorterStemmer

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      if os.path.isfile('data.pkl'):
         pkl=self.load('data.pkl')
         #get the whole data from data.pkl file
         self.pos={}
         self.neg={}
         self.numPos=pkl[0]
         self.numNeg=pkl[1]
         self.pos=pkl[2]
         self.neg=pkl[3]
      else:
         #initiate the variables
         self.pos={}
         self.neg={}
         self.numPos = 0
         self.numNeg = 0
      self.useless = {"i":0,"you":0,"she":0,"he":0,"they":0,"it":0,"the":0,"a":0,"an":0}
      #,"which":0,"what":0,"where":0,"that":0,"this":0,"mine":0,"my":0,"your":0,"her":0,"his":0,"their":0

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      if os.path.isfile('data.pkl')==False:
         IFileList=[]
         stemmer=PorterStemmer()
         for fFileObj in os.walk("movies_reviews/"):
            IFileList = fFileObj[2]
            break

         for i in range(len(IFileList)):
            splitList = IFileList[i].split('-')
            token = self.loadFile(str("movies_reviews/")+IFileList[i])
            token = token.lower()
            #lower the whole sentence
            tokens = self.tokenize(token)
            setTokens = set(tokens)
            tokens = [i for i in setTokens]
            if splitList[1] == "5":
               #while the review is a positive review
               self.numPos+=1
               for j in range(len(tokens)):
                  flag = 0
                  for char in tokens[j]:
                     if ord(char)>127:
                        #if the character is a French character
                        flag = 1
                        break
                  tokenLen = len(tokens[j])
                  if flag == 0:
                     tokens[j] = str(stemmer.stem(tokens[j]))
                     # get the stem of a word
                     if tokens[j][tokenLen-3 : tokenLen] == "n't" or tokens[j] == "not":
                        if j+1 <= len(tokens)-1:
                           tokens[j] = "not"
                           tokens[j+1] = str(stemmer.stem(tokens[j+1]))
                           tokens[j+1] = tokens[j] + tokens[j+1]
                           j += 1
                     if self.useless.has_key(tokens[j]) == False:
                        #if the word is in useless, delete it
                        if self.pos.has_key(tokens[j]):
                           self.pos[tokens[j]]+=1
                        else:
                           self.pos[tokens[j]]=1
            if splitList[1]=="1":
               #while the review is a positive review
               self.numNeg+=1
               for j in range(len(tokens)):
                  flag = 0
                  for char in tokens[j]:
                     if ord(char)>127:
                        #if the character is a French character
                        flag = 1
                        break
                  tokenLen = len(tokens[j])
                  if flag == 0:
                     tokens[j] = str(stemmer.stem(tokens[j]))
                     # get the stem of a word
                     if tokens[j][tokenLen-3 : tokenLen] == "n't" or tokens[j] == "not":
                        if j+1 <= len(tokens)-1:
                           tokens[j] = "not"
                           tokens[j+1] = str(stemmer.stem(tokens[j+1]))
                           tokens[j+1] = tokens[j] + tokens[j+1]
                           j += 1
                     if self.useless.has_key(tokens[j]) == False:
                        #if the word is in useless, delete it
                        if self.neg.has_key(tokens[j]):
                           self.neg[tokens[j]]+=1
                        else:
                           self.neg[tokens[j]]=1

         print self.numPos
         print self.numNeg
         list1=[]
         list1.append(self.numPos)
         list1.append(self.numNeg)
         list1.append(self.pos)
         list1.append(self.neg)
         #save the whole data to data.pkl file
         self.save(list1,'data.pkl')
    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      sumPos = 0.0
      sumNeg = 0.0
      sumAll = 0.0
      sText = sText.lower()
      tokens = self.tokenize(sText)
      setTokens = set(tokens)
      tokens = [i for i in setTokens]
      strPos = self.pos.keys()
      stemmer=PorterStemmer()
      for i in range (len(self.pos)):
         sumAll += self.pos[strPos[i]]+self.neg[strPos[i]]
      for i in range (len(tokens)):
         flag = 0
         for char in tokens[i]:
            if ord(char)>127:
               #if the character is a French character
               flag = 1
               break
         tokenLen = len(tokens[i])
         if flag == 0:
            tokens[i] = str(stemmer.stem(tokens[i]))
            # get the stem of a word
            if tokens[i][tokenLen-3 : tokenLen] == "n't" or tokens[i] == "not":
               if i+1 <= len(tokens)-1:
                  tokens[i] = "not"
                  tokens[i+1] = tokens[i] + tokens[i+1]
                  i += 1 
            if self.pos.has_key(tokens[i])==False:
               self.pos[tokens[i]]=0
            if self.neg.has_key(tokens[i])==False:
               self.neg[tokens[i]]=0
            sumPos += math.log(float(self.pos[tokens[i]]+1)/float(self.numPos))
            sumNeg += math.log(float(self.neg[tokens[i]]+1)/float(self.numNeg))
            #compute the probability of positive and negative
      if sumPos >= sumNeg:
         #judge whether the review is positive or negative
         return "Positive"
      else:
         return "Negative"

   def evaluation(self):
      self.averageNumPos = int(math.ceil (self.numPos/10))
      self.averageNumNeg = int(math.ceil (self.numNeg/10))
      listPer = []

      for i in range(10):
         #for each one
         setfold = ([0,1,2,3,4,5,6,7,8,9])
         setfold.remove(i)
         #evaluate 90%
         listPer.append(self.evaluationHelp(setfold,i))
         """i=0
      setfold = ([0,1,2,3,4,5,6,7,8,9])
      self.currentfold = i
      setfold.remove(i)
      print i
      #evaluate 90%
      listPer.append(self.evaluationHelp(setfold,i))"""
      print listPer
      averageEval = sum(listPer)/ len(listPer)
      return averageEval
   
   def evaluationHelp(self, setfold, n) :
      print setfold
      print n
      for i in range (9):
         downNum = setfold[i] * self.averageNumNeg
         upNum = (setfold[i]+1) * self.averageNumNeg
         self.trainHelp(setfold,n,downNum,upNum,"negative")
      for i in range (9):
         downNum = setfold[i] * self.averageNumPos + self.numNeg
         upNum = (setfold[i]+1) * self.averageNumPos +self.numNeg
         self.trainHelp(setfold,n,downNum,upNum,"positive")
      for fFileObj in os.walk("movies_reviews/"):
         IFileList = fFileObj[2]
         break
      correct=0
      correctFile=0
      #positive
      pkl=self.load(str(n)+'.pkl')
      self.pos={}
      self.neg={}
      self.pos=pkl[0]
      self.neg=pkl[1]

      downNum = n * self.averageNumPos + self.numNeg
      upNum = (n+1) * self.averageNumPos +self.numNeg
      q = downNum
      print "3D"+str(downNum)
      print "U"+str(upNum)
      while q < upNum and q < self.numPos+self.numNeg:
         correctFile+=1
         a=self.loadFile("movies_reviews/"+IFileList[q])
         splitList = IFileList[q].split('-')
         if (self.classifyT(a) == "Positive" and str(splitList[1]) == "5") or (self.classifyT(a) == "Negative" and str(splitList[1]) == "1"):
            correct+=1
         q+=1
      #negative
      downNum = n * self.averageNumNeg
      upNum = (n+1) * self.averageNumNeg
      j = downNum
      print "4D"+str(downNum)
      print "U"+str(upNum)
      while j < upNum and j < self.numNeg:
         correctFile+=1
         a=self.loadFile("movies_reviews/"+IFileList[j])
         splitList = IFileList[j].split('-')
         if (self.classifyT(a) == "Negative" and str(splitList[1]) == "1")or(self.classifyT(a) == "Positive" and str(splitList[1]) == "5"):
            correct+=1
         j+=1
      print "C"+str(correct)
      print "C"+str(correctFile)
      percent=float(correct)/float(correctFile)
      print percent
      return percent
      #k=0
      #while ( k >= setfold[n] *self.averageNumPos and k <= setfold[n+1] and k <self.numPos):
      #   classify()

   def classifyT(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      sumPos = 0.0
      sumNeg = 0.0
      sText = sText.lower()
      tokens = self.tokenize(sText)
      setTokens = set(tokens)
      tokens = [i for i in setTokens]
      strPos = self.pos.keys()
      stemmer=PorterStemmer()
      for i in range (len(tokens)):
         flag = 0
         for char in tokens[i]:
            if ord(char)>127:
               #if the character is a French character
               flag = 1
               break
         tokenLen = len(tokens[i])
         if flag == 0:
            tokens[i] = str(stemmer.stem(tokens[i]))
            # get the stem of a word
            if tokens[i][tokenLen-3 : tokenLen] == "n't" or tokens[i] == "not":
               if i+1 <= len(tokens)-1:
                  tokens[i] = "not"
                  tokens[i+1] = tokens[i] + tokens[i+1]
                  i += 1 
            if self.pos.has_key(tokens[i])==False:
               #if the word is in useless, delete it
               self.pos[tokens[i]]=0
            if self.neg.has_key(tokens[i])==False:
               self.neg[tokens[i]]=0
            sumPos += math.log(float(self.pos[tokens[i]]+1)/(float(self.numPos)*0.9))
            sumNeg += math.log(float(self.neg[tokens[i]]+1)/(float(self.numNeg)*0.9))
            #compute the probability of positive and negative
      #print sumPos
      #print sumNeg
      if sumPos >= sumNeg:
         #judge whether the review is positive or negative
         return "Positive"
      else:
         return "Negative"

   def trainHelp(self,setfold,num,downNum,upNum,judge):   
      """Trains the Naive Bayes Sentiment Classifier."""
      if os.path.isfile(str(num)+'.pkl')==True:
         pkl=self.load(str(num)+'.pkl')
         self.pos={}
         self.neg={}
         self.pos=pkl[0]
         self.neg=pkl[1]
      else:
         #initiate the variables
         self.pos={}
         self.neg={}
         
      IFileList=[]
      stemmer=PorterStemmer()
      for fFileObj in os.walk("movies_reviews/"):
         IFileList = fFileObj[2]
         break
      #for i in range(len(IFileList)):
      i = downNum 
      if judge == "positive":
         self.Max = self.numPos +self.numNeg
      else:
         self.Max = self.numNeg
      while i < upNum and i < self.Max:
         splitList = IFileList[i].split('-')
         if splitList[1] == "5":
            #while the review is a positive review
            token = self.loadFile(str("movies_reviews/")+IFileList[i])
            token = token.lower()
            #lower the whole sentence
            tokens = self.tokenize(token)
            setTokens = set(tokens)
            tokens = [p for p in setTokens]
            for j in range(len(tokens)):
               flag = 0
               for char in tokens[j]:
                  if ord(char)>127:
                     #if the character is a French character
                     flag = 1
                     break
               tokenLen = len(tokens[j])
               if flag == 0:
                  tokens[j] = str(stemmer.stem(tokens[j]))
                  # get the stem of a word
                  if tokens[j][tokenLen-3 : tokenLen] == "n't" or tokens[j] == "not":
                     if j+1 <= len(tokens)-1:
                        tokens[j] = "not"
                        tokens[j+1] = tokens[j] + tokens[j+1]
                        j += 1
                  if self.useless.has_key(tokens[j]) == False:
                     #if the word is in useless, delete it
                     if self.pos.has_key(tokens[j]):
                        self.pos[tokens[j]]+=1
                     else:
                        self.pos[tokens[j]]=1
         else:
            #while the review is a positive review
            token = self.loadFile(str("movies_reviews/")+IFileList[i])
            token = token.lower()
            #lower the whole sentence
            tokens = self.tokenize(token)
            setTokens = set(tokens)
            tokens = [p for p in setTokens]
            for j in range(len(tokens)):
               flag = 0
               for char in tokens[j]:
                  if ord(char)>127:
                     #if the character is a French character
                     flag = 1
                     break
               tokenLen = len(tokens[j])
               if flag == 0:
                  tokens[j] = str(stemmer.stem(tokens[j]))
                  # get the stem of a word
                  if tokens[j][tokenLen-3 : tokenLen] == "n't" or tokens[j] == "not":
                     if j+1 <= len(tokens)-1:
                        tokens[j] = "not"
                        tokens[j+1] = tokens[j] + tokens[j+1]
                        j += 1
                  if self.useless.has_key(tokens[j]) == False:
                     #if the word is in useless, delete it
                     if self.neg.has_key(tokens[j]):
                        self.neg[tokens[j]]+=1
                     else:
                        self.neg[tokens[j]]=1
         i+=1
            
      #print self.numPos
     # print self.numNeg
      list1=[]
      list1.append(self.pos)
      list1.append(self.neg)
      #save the whole data to data.pkl file
      self.save(list1,str(num)+'.pkl')

   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c=="'" or c == "_":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens
