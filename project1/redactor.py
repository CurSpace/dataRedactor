import argparse
import os
import re 
import spacy
from spacy import displacy
import nltk
import glob
from commonregex import CommonRegex
# named entity recognition using spacy
nlp = spacy.load("en_core_web_sm")


nltk.download('words')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger')
nltk.download('all')

#from nltk.corpus import stopwords
from nltk.corpus import wordnet 
from nltk.tokenize import word_tokenize,sent_tokenize
#from nltk import ne_chunk

# the user can input multiple files
def input_files(files_in):
    '''
    if the target token is next to \n or there special characters it leads to incorrect label assignment there for removing \n and other special characters
    '''
    if len(files_in) == 0:
        raise Exception('No files given\n')
    files_together = []
    all_data = []
    # make nested list into list
    files_in = nltk.flatten(files_in)
    for text_files in files_in:

            lst_fls = glob.glob(text_files)

            for each_file in lst_fls:
                data = open(each_file,"r").read()
                data = data.replace("\\"," ")
                data = data.replace("\n"," ")
                data = data.replace("_"," ")
                all_data.append(data)
                all_data.append("filesep")
   
    all_data = str(all_data)
    return all_data
def redact_all_names(data):
    '''
    does not redact uncommon names like Ermis 
    does not redact name if it appears in the email address
    Eventhough it redacts common names like Frank spacy incorrectly assigns label PERSON to ['Frank Ermis Jan2002', 'Frank Inbox X-Origin']
    '''
    type_of = "Names:"
    doc = nlp(data)
    names =  [ent.text for ent in doc.ents if ent.label_ == 'PERSON' ]
    for name in names:
           
         data = re.sub(name,'\u2588' * len(name), data)
    count = len(names)   
    get_stats(type_of, count)
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
    print(redacted_dates)
    print(data)
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
    print(redacted_numbers)   
    for number in redacted_numbers:
        data = data.replace(number,'\u2588' * len(number))
   # print(data)
    count = len(redacted_numbers) 
    get_stats(type_of,count)
    print(data)
    return data
    

def redact_all_genders(data):
    type_of = "Genders:"
    data = str(data)
    gender_indicators = ['HE','HIM','SHE','HER','FATHER','MOTHER','MOM','DAD','MUMMY','DADDY', 'BROTHER','SISTER','UNCLE','AUNT', 'BOY', 'GIRL', 'BOYFRIEND','GIRLFRIEND','POP','MEN','WOMEN','ACTOR','ACTRESS','NIECE','NEPHEW'] 
    tokens = nltk.word_tokenize(data)
   
    count = 0
    for word in tokens:   
       if word.upper() in gender_indicators:
            data = data.replace(word,"\u2588" * len(word))
            count = count + 1
    
    get_stats(type_of,count)
    print(data)
    return data


def redact_all_addressess(data):
   type_of ="Addressess:"
   addressess =re.findall(r'\d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}' ,data)
   print(addressess) 
   for address in addressess:
        data = data.replace(address,'\u2588' * len(address))
   print(data)
   count = len(addressess)

   get_stats(type_of,count)
   return data
     

def redact_all_concepts(data,concept):
     data = list(nltk.flatten(data))
     type_of = "Concepts:"
     list_of_syns = []
     concept_list = []
     concept_list =str(nltk.flatten( nltk.flatten(concept_list.append(concept))))
     count = 0
     for concept in concept_list:
         for syn in wordnet.synsets(concept_list):
             synonyms.append(syn.lemma_names())
             for lemma in syn.hyponyms():
                 synm = lemma.lemma_names()
                 list_of_syns.append(synm)

     synonyms = list(nltk.flatten(list_of_syns))
     for c in concept:
         synonyms.append(c)
        
     redacted_data = []
     for dat in data:
         doc = nlp(dat)
         for sents in doc.sents:
             for concept in synonyms:
                 if concept in str(sents):
                        
                     dat = dat.replace(str(sents),"\n"+ u"\u2588"*len(str(sents)))
                     count = count + 1   
         redacted_data.append(dat)
   
     redacted_data = str(redacted_data)
     get_stats(type_of,count)
     return redacted_data


def redacted_output(files_in,data,redacted_file):
     
    data = data.split("filesep")
    lst_files = []
    for i in files_in:
        for file in i:
            lst_files.append(glob.glob(file))
    flat = nltk.flatten(lst_files)
    # save redacted file in current working directory
    files_at = os.path.join(os.getcwd(), redacted_file)
    # replace imput file extension with .redacted
    filen = 0
    while filen < len(flat):
      
        ipath = os.path.splitext(flat[filen])[0]
        ipath = os.path.basename(ipath) + ".redacted"
   
        if not os.path.exists(files_at):
            os.makedirs(files_at)
            with open(os.path.join(files_at,ipath), 'w') as output:
                output.write(data[filen])
    
        elif os.path.exists(files_at):
            with open(os.path.join(files_at, ipath), 'w') as output:
                output.write(data[filen])
        filen = filen +1

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

    if type_of == "Addressess":
        store_stats.append(type_of + str(count))

    if type_of == "Concepts:":
        store_stats.append(type_of + str(count))


    return store_stats



def write_stats(path,store_stats):
    '''
    Creates a file in the current working directory and writes the stats to the file
    '''
    stat = 0 
    
    path = os.path.join(os.getcwd(), path)
    statsfile = open(path,'w')
    while stat <= (len(store_stats) -1) :
        statsfile.write(store_stats[stat])
        statsfile.write('\n')
        stat = stat + 1
    statsfile.close()
    return store_stats
  
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

    if args.output:
        redacted_output(args.input, data, args.output)
  
    if args.names:
    
        data = redact_all_names(data)
                     
    if args.dates:
        
        data = redact_all_dates(data)
    if args.phones:
        
        data = redact_all_phonenumbers(data)
    if args.genders:
        
        data = redact_all_genders(data)
    if args.concept:
        data = redact_all_concepts(data, args.concept)  
    
    if args.address:
        data = redact_all_addressess(data)

    redacted_output(args.input, data, args.output)

    if args.stats:
        write_stats(args.stats,store_stats)


