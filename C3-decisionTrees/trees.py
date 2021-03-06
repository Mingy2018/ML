from math import log
import operator
import matplotlib.pyplot as plt

def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={} # list
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys(): # return the keys of the list
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for keys in labelCounts:
        prob=float(labelCounts[keys]/numEntries)
        shannonEnt-=prob*log(prob,2) # definition of Shannon entropy
    return shannonEnt

def createDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
    labels=['no surfacing','flippers'] #the labels of features
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    '''
    @dataSet: the dataset we'll split
    @axis: the features
    @value:
    '''
    retdataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:]) # 将该样本的分类特征删除
            retdataSet.append(reducedFeatVec)# 将该样本作为一个元素，添加到list中
    return retdataSet


def chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1 #take the length of one sample, minus the labels= number of features
    baseEntropy=calcShannonEnt(dataSet)
    bestIofoGain=0.0; bestFeature=-1
    for i in range(numFeatures): # from every features
        # Create unique list of class labels
        featList=[example[i] for example in dataSet] # take the value of current feature of all samples in dataset
        uniqueVals=set(featList) #cancle the repeated element to only one
        newEntropy=0.0
        # Calculate entropy for each split
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        # Find the best information gain
        if (infoGain>bestIofoGain):
            bestIofoGain=infoGain
            bestFeature=i
        return bestFeature




def majorityCnt(classList):
    classCount={} # define a empty dictionaries
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),
                            key=operator.itemgetter(1),reverse=True)
    # @reverse: True-descending
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    # create a list of all the class labels in the data set
    classList=[example[-1] for example in dataSet]
    # Stop when all classes are equal-> 只存在一种分类，代表分类完全，可以结束
    if classList.count(classList[0])==len(classList): # if all the class labels are same
        return classList[0]
    # when no more features to split, return majority
    if len(dataSet[0])==1:
        return majorityCnt(classList)

    bestFeat=chooseBestFeatureToSplit(dataSet) # the int number at which the feature is
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}} # define dictionary
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues) # 提高运算效率
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createDataSet(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree



