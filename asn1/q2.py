__author__ = 'Si Yi Wu'

def rotate_word( word,i):
    if len(word) <= i:
        return word
    else:
        return word[i:] + word [0:i]

