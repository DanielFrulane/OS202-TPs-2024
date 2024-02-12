import random
import time
import threading

numberOfValues = 10000000
numberOfBuckets = 8
rangeOfValuesMin = 0
rangeOfValuesMax = 10

def generateRandomvalueList(nValues, min, max):
    randomValueList = [random.uniform(min, max) for _ in range(nValues)]
    return randomValueList


def bucketSort(valueList, nBuckets, min, max):
    # dividing values into buckets
    intervalStep = nBuckets/(max - min)
    buckets = []
    for index in range(numberOfBuckets):
        buckets.append([])
    for value in valueList:
        valueConvertedToIndex = int(intervalStep*value)
        buckets[valueConvertedToIndex].append(value)

    # generic sort
    for index in range(len(buckets)):
        buckets[index] = sorted(buckets[index])

    # gathering results
    finalList = [None] * len(valueList)
    index = 0
    for bucket in buckets:
        for i in range(len(bucket)):
            finalList[index] = bucket[i]
            index += 1
    return finalList


def worker(listOfValues):
    # generic sort
    return sorted(listOfValues)

class BucketThreading:
    def __init__(self,bucketList,n):
        self.buckets = bucketList
        self.numberOfThreads = n
        self.threads = []

    def sort(self):
        for i in range(self.n):
            t = threading.Thread(target=worker, args=(self.buckets[i]))
            t.start()
            self.threads.append(t)
        for t in self.threads:
            t.join()
    
def bucketSortThreaded(valueList, nBuckets, min, max):
    # dividing values into buckets
    intervalStep = nBuckets/(max - min)
    buckets = []
    for index in range(numberOfBuckets):
        buckets.append([])
    for value in valueList:
        valueConvertedToIndex = int(intervalStep*value)
        buckets[valueConvertedToIndex].append(value)

    # threaded sort
    BucketThreading(buckets, numberOfBuckets)

    # gathering results
    finalList = [None] * len(valueList)
    index = 0
    for bucket in buckets:
        for i in range(len(bucket)):
            finalList[index] = bucket[i]
            index += 1
    return finalList


def main():
    valueList = generateRandomvalueList(numberOfValues, rangeOfValuesMin, rangeOfValuesMax)

    start = time.time()
    ordedList = bucketSort(valueList, numberOfBuckets, rangeOfValuesMin, rangeOfValuesMax)
    finish = time.time()
    timeElapsed = finish - start
    formatted_num = f"{timeElapsed:.2e}"
    print("Bucket Sort without threads sorted list in: " + formatted_num + " seconds")

    start = time.time()
    ordedList = bucketSortThreaded(valueList, numberOfBuckets, rangeOfValuesMin, rangeOfValuesMax)
    finish = time.time()
    timeElapsed = finish - start
    formatted_num = f"{timeElapsed:.2e}"
    print("Bucket Sort with threads sorted list in: " + formatted_num + " seconds")

main()