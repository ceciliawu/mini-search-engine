__author__ = 'Si Yi Wu'

import operator

class fileIterator:
    def __init__(self,file_name):
        self.file_name = file_name
        self.file = open(file_name,'r')
        self.words = []

    def __iter__ (self):
        return self

    def next(self):
        if (len(self.words) == 0):
            line = self.file.next()
            self.words = line.split()
        if (len(self.words) > 0):
            return self.words.pop(0)



def find_popular(file_name):
    word_iter = fileIterator(file_name)
    word_dic = {}

    for w in word_iter:
        if w in word_dic:
            word_dic[w] += 1
        else:
            word_dic[w] = 1

    sorted_word = sorted(word_dic.items(),key = operator.itemgetter(1),reverse = True)

    top_10_words =  sorted_word[0:10]
    for (key,value) in top_10_words:
        print key




if __name__ == "__main__":
    find_popular("q4test.txt")




