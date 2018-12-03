__author__ = 'Si Yi Wu'


import re
def split_sentence (file_name):
    file = open(file_name).read()
    file = file.replace('\n',' ')
    file = file.replace('\r','')

    splitted = re.split(r'(?<=[^A-Z].[.?!]) +(?=[A-Z])', file)


    output_file = open('q5.out','w+')

    for i in splitted:
        output_file.write(i)
        output_file.write('\n')




if __name__ == "__main__":
    split_sentence('q5test.txt')
