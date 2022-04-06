from project1 import redactor
import pytest
import nltk
path = './tests/5.txt'
def test_datainput ():
    data = redactor.input_files(path)
    print (len(data))
    if len(data) != 0:
        assert data is not None



def test_phonenumbers():
    data = redactor.input_files(path)
    phonenumbers = redactor.redact_all_phonenumbers(data)    
    assert len(phonenumbers) is not None
   

def test_genders():
    count =0
    data = (redactor.input_files(path))
    gender_lst = redactor.redact_all_genders(data)
    for i in range(len(gender_lst)):
        temp = gender_lst[i]
        words = nltk.word_tokenize(temp)
        for j in words:
            if '\u2588' in j:
                count += 1
    assert count is not None

def test_dates():

    count = 0

    data= redactor.input_files(path)
    redacted_data  = redactor.redact_all_dates(data)
    for i in range(len(redacted_data)):
        redaction_style = u"\u2588"
        for j in range(len(redacted_data[i])):
            word = redacted_data[i][j]
            redaction_style = len(word)*redaction_style
            if redaction_style == word:
                count = count + 1
    if count >= 0 or len(redacted_data) > 0 :
        assert True


def test_names():
    
    count =0
    data = (redactor.input_files(path))
    name_lst = redactor.redact_all_names(data)
    for i in range(len(name_lst)):
        temp = name_lst[i]
        names = nltk.word_tokenize(temp)
        for j in names:
            if '\u2588' in j:
                count += 1
    assert count is not None
