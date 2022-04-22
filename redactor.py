import argparse
import os
import re 
import spacy
from spacy import displacy
import nltk
import glob
from commonregex import CommonRegex
import sys
# named entity recognition using spacy
import en_core_web_md
nlp = en_core_web_md.load()
#nlp = spacy.load("en_core_web_sm")
nltk.download('wordnet')
nltk.download('omw-1.4')
#nltk.download('words')
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('maxent_ne_chunker')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('all')
from itertools import chain

from nltk.corpus import wordnet 
from nltk.tokenize import word_tokenize,sent_tokenize


# the user can input multiple files
def input_files(files_in):
    '''
    if the target token is next to \n or there special characters it leads to incorrect label assignment there for removing \n and other special characters
    '''
    if len(files_in) == 0:
        raise Exception('No files given\n')
    files_together = []
    all_data = ""
    # make nested list into list
    files_in = nltk.flatten(files_in)
    for text_files in files_in:

            lst_fls = glob.glob(text_files)

            for each_file in lst_fls:
                data = open(each_file,"r").read()
                #data = data.replace("\\","")
                data = data + "!@#$%^&*("
                all_data = ''.join([all_data,data])
             #   data = data + "&&%#&*&"
               # data = data.replace("\n"," ")
               # data = data.replace("_"," ")
                
                #all_data.append("\t+")
   
    
   # print(all_data)
    return all_data
def redact_all_names(data):
    '''
    does not redact uncommon names like Ermis 
    does not redact name if it appears in the email address
    Eventhough it redacts common names like Frank spacy incorrectly assigns label PERSON to ['Frank Ermis Jan2002', 'Frank Inbox X-Origin']
    '''
    type_of = "Names:"
    doc = nlp(data)
    names = []
    for ent in doc:
       # print(ent.text)
        if ent.ent_type_ =='PERSON':
            names.append(ent.text) 
  #  names =  [ent.text for ent in doc.ents if ent.label_ == 'PERSON' ]
    #print(names)   
    for name in names:
           
         data = re.sub(name,'\u2588' * len(name), data)
    count = len(names)
   # print(names,count)
    get_stats(type_of, count)
   # print(data)
    return data

 
def redact_all_dates(data):
    '''
    correctly matches dates like this 25 Nov 2001
    incorrectly matches like ['26 Nov 0001', '4-20-7783', '1-2-9229'] sections phone numbers but does not redact them because it matches a subsection of the token
    '''
    type_of = "Dates:"
    
    redacted_dates = CommonRegex(data).dates
    
    for date in redacted_dates:
        
         data = re.sub('\\b{}\\b'.format(date),'\u2588' * len(date), data)
    count = len(redacted_dates)
   # print(redacted_dates)
   # print(data)
    get_stats(type_of,count)
    return data

def redact_all_phonenumbers(data):
    '''
    redacts wrong 2 numbers at the start ['5941235', '1075855165188', '(713) 345-4727']
    won't redact phones of the format +61-2-9229-2336
    correctly matches phonenubmers of the format (713) 345-4727 
    '''
    type_of = "Phones:"
    
    redacted_numbers = CommonRegex(data).phones
   # print(redacted_numbers)   
    for number in redacted_numbers:
        data = data.replace(number,'\u2588' * len(number))
   # print(data)
    count = len(redacted_numbers) 
    get_stats(type_of,count)
   # print(data)
    return data
    

def redact_all_genders(data):
    type_of = "Genders:"
    gender_indicators = ['HE','HIM','SHE','HER','FATHER','MOTHER','MOM','DAD','MUMMY','DADDY', 'BROTHER','SISTER','UNCLE','AUNT', 'BOY', 'GIRL', 'BOYFRIEND','GIRLFRIEND','POP','MEN','WOMEN','ACTOR','ACTRESS','NIECE','NEPHEW','wife','husband','boy','girl','man','woman','he','she','daughter','son','niece','nephew','aunt','mother','male','female','girlfriend','boyfriend','gentlemen','gentlewoman','brother','sister','grandmother','grandfather','granddaughter','bride','groom','sir','grandma','grandpa','grandmom','herself','himself','queen','king','princess','prince','women','widower','widow','fiancee','fiance','herione','hero','herione','god','goddess','lord','lady','chairman','chairwoman'] 
   # tokens = nltk.word_tokenize(data)
   
  #  count = 0
  #  for word in tokens:   
  #     if word.upper() in gender_indicators:
  #          data = data.replace(word,"\u2588" * len(word))
  #          count = count + 1
    
  #  get_stats(type_of,count)
   # print(data)i
#    reg = re.compile(r"\b(?:(" + "(')?s?)|(".join(gender_indicators) + r"))\b", flags=re.I)
    
    counts = 0
    for gender in gender_indicators:
       

            data,c = re.subn("\\b{}\\b|\\b{}s\\b|\\b{}'s\\b".format(gender,gender,gender) , '\u2588'*len(gender), data, flags = re.I,count =0)
            counts = counts + c
    get_stats(type_of,counts)

    
    return data


def redact_all_addressess(data):
   
    type_of ="Addressess:"
   # pattern = '(\d{1,6}[A-Za-z]?\s(?:[A-Za-z0-9#-]+\s){0,7}(?:[A-Za-z0-9#-]+,)\s(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s[A-Z]{2}\s*\d{4,5})'
# addressess =re.findall(r'\d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}' ,data)
  #  addressess =re.findall('(\d{1,6}[A-Za-z]?\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s([A-Z]{2})\s(\d{4,5})*)' ,data)
    # findall gives empty str for no match   
    addressess =re.findall('(\d{1,6}[A-Za-z]?\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,*)\s([A-Z]{2})*\s*\d{4,5})' ,data)
 
    
   # if len(addressess) > 0:
   # print(addressess)   
    for address in addressess:
    
        if len(address) > 0:
               
            i = '\u2588' * len(address[0])
        
            data = re.sub(address[0],i, data )
  # print(data)
    count = len(addressess)
    get_stats(type_of,count)
    return data
     

def redact_all_concepts(data,concept):
    '''
    repace every new line with .
    '''
   # doc = nlp(data)
   # for sentence in doc.sents:
   #     print("INSIDE for")
   #     print(sentence.text)
    con =  concept[0][0] 
    synonyms = [[con]]
    type_of = "Concepts:"
    counts = 0

    x=[]
    for hypo in  wordnet.synsets(con)[0].hyponyms():
        synonyms.append(hypo.lemma_names())

    for syn in wordnet.synsets(con):
        for l in syn.lemmas():
            x.append(l.name())
        synonyms.append(x)    

    synonyms = list(chain.from_iterable(synonyms))
    data1 = data.replace("\n",". ")   
    sentences = data1.split(". ")
    sentences = list(filter(None,sentences))
    
    for sent in sentences:
        for con in synonyms:
            match = re.findall(con,sent,flags = re.I)
           
            if len(match) > 0:
                replace = '\u2588'* len(sent)
                data,c = re.subn(sent, replace ,data,count = 0)
                counts = counts + c
   # print(counts)
    get_stats(type_of,counts)    
    for syn in synonyms:

        data = re.sub(syn,'\u2588' * len(syn),data )

    return data
def redacted_output(files_in,data,redacted_file):
   # print("BEFORE SPLIT\n\n\n",data) 
    data = data.split("!@#$%^&*(")
   # print(len(data))
  
    lst_files = []
    for i in files_in:
        for file in i:
            lst_files.append(glob.glob(file))
    flat = nltk.flatten(lst_files)
   # print(flat)
    # save redacted file in current working directory
    files_at = os.path.join(os.getcwd(), redacted_file)
    # redacted_file = file name that the user inputs
   #files_at =  home/callpradip96/cs5293sp22-project1/project1/t
   # print(files_at)
    # replace imput file extension with .redacted
    filen = 0
   # print(len(flat))
    while filen < len(flat):
      
       # ipath = os.path.splitext(flat[filen])[0]
        ipath = os.path.basename(flat[filen]) + ".redacted"
   
        if not os.path.exists(files_at):
            os.makedirs(files_at)
            with open(os.path.join(files_at,ipath), 'w') as output:
      #          print(data[filen])
                output.write(data[filen])
    
        elif os.path.exists(files_at):
            with open(os.path.join(files_at, ipath), 'w') as output:
              #  print(data[filen])
                output.write(data[filen])
     #   print("BEFORE",filen)
        filen += 1
    
store_stats = []
def get_stats(type_of,count):
    count = str(count)
    if type_of == "Names:":
        
        store_stats.append(type_of + str(count))
     
    if type_of == "Dates:":
        store_stats.append(type_of + str(count))
        

    if type_of == "Phones:":
        store_stats.append(type_of + str(count))

    if type_of == "Genders:":
        store_stats.append(type_of + str(count))

    if type_of == "Addressess:":
        store_stats.append(type_of + str(count))

    if type_of == "Concepts:":
        store_stats.append(type_of + str(count))

    
    return store_stats



def write_stats(pathd,store_stats):
    '''
    Creates a file in the current working directory and writes the stats to the file
    '''
  #  print(store_stats)   

    # create a folder and write a file inside it
   

    if(pathd != 'stdout' and pathd != 'stderr' ):
    
    
        with open(pathd,'w') as statout:
            for stat in store_stats:
                statout.write(stat)
                statout.write('\n')
        statout.close()
    else:
        for stat in store_stats:
            if(pathd == 'stdout'):
                sys.stdout.write(stat)      
                sys.stdout.write('\n')
            if(pathd == 'stderr'):
                sys.stderr.write(stat)
                sys.stderr.write('\n')
    
if __name__ == "__main__":

    arguments = argparse.ArgumentParser()
    arguments.add_argument("--input",type = str, required = True, help = "path to input files", nargs = "*", action = "append" )
    arguments.add_argument("--names", required = False, help = "option to redate names", action = "store_true")
    arguments.add_argument("--genders", required = False, help = "option to redact genders", action = "store_true")
    arguments.add_argument("--dates", required = False, help = "option to redact dates", action = "store_true")
    arguments.add_argument("--phones", required = False, help = "option to redact phone numbers", action = "store_true")
    arguments.add_argument("--address", required = False, help = "option to redact address", action = "store_true")
    # can be repeated multiple times
    arguments.add_argument("--concept", type = str, required = False, help = "option to redact concepts", nargs= "*", action = "append")
    arguments.add_argument("--stats", type = str, required = False, help = "option to to print stats for redactions")
    arguments.add_argument("--output", type = str, required = True, help = "path  to outputfile")
    args = arguments.parse_args()

    data  = input_files(args.input)

    if args.concept:
        data = redact_all_concepts(data, args.concept)
  
    if args.phones:
        data = redact_all_phonenumbers(data)
    
    if args.address:
        data = redact_all_addressess(data)

    if args.dates:
        data = redact_all_dates(data)

    if args.genders:
        data = redact_all_genders(data)

    if args.names:
        data = redact_all_names(data)
                     
    if args.stats:
        write_stats(args.stats,store_stats)
    if args.output:
        redacted_output(args.input, data, args.output)

