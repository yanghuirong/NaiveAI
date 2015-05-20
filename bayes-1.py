# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re , operator, nltk

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      if os.path.isfile('data.pkl'):
         pkl=self.load('data.pkl')
         self.pos={}
         self.neg={}
         self.pos=pkl[0]
         self.neg=pkl[1]
      else:
         self.pos={}
         self.neg={}
      

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      if os.path.isfile('data.pkl')==False:
         IFileList=[]
         for fFileObj in os.walk("movies_reviews/"):
            IFileList = fFileObj[2]
            break
         useless = {"i":0,"you":0,"she":0,"he":0,"they":0,"it":0,"the":0,"a":0,"an":0}
         for i in range(len(IFileList)):
            splitList = IFileList[i].split('-')
            if splitList[1] == "5":
               token = self.loadFile(str("movies_reviews/")+IFileList[i])
               token = token.lower()
               tokens = self.tokenize(token)
               for j in range(len(tokens)):
                  if useless.has_key(tokens[j]) == False:
                     if self.pos.has_key(tokens[j]):
                        self.pos[tokens[j]]+=1
                     else:
                        self.pos[tokens[j]]=1
                     if self.neg.has_key(tokens[j])==False:
                        self.neg[tokens[j]]=0
            if splitList[1]=="1":
               token = self.loadFile(str("movies_reviews/")+IFileList[i])
               token = token.lower()
               tokens = self.tokenize(token)
               for j in range(len(tokens)):
                  if useless.has_key(tokens[j]) == False:
                     if self.neg.has_key(tokens[j]):
                        self.neg[tokens[j]]+=1
                     else:
                        self.neg[tokens[j]]=1
                     if self.pos.has_key(tokens[j])==False:
                        self.pos[tokens[j]]=0
         print len(self.pos)
         print len(self.neg)
         list1=[]
         list1.append(self.pos)
         list1.append(self.neg)      
         self.save(list1,'data.pkl')
    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      sumPos = 0.0
      sumNeg = 0
      sumAll = 0.0
      sText = sText.lower()
      tokens = self.tokenize(sText)
      strPos = self.pos.keys()
      for i in range (len(self.pos)):
         sumAll += self.pos[strPos[i]]+self.neg[strPos[i]]
      for i in range (len(tokens)):
         if self.pos.has_key(tokens[i])==False:
            self.pos[tokens[i]]=0
            self.neg[tokens[i]]=0
         sumPos += math.log(float(self.pos[tokens[i]]+1)/float(sumAll))
         sumNeg += math.log(float(self.neg[tokens[i]]+1)/float(sumAll))
      print sumPos
      print sumNeg
      if sumPos >= sumNeg:
         return "Positive"
      else:
         return "Negtive"


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
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
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
