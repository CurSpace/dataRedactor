# Data Redactor
### Author : Pradipkumar Rajasekaran

__Summary:__

The goal of this project is to redact data from text files. The text files contain Emails from the Enron scandal. The text file is given as input,
which is cleaned and taken as a string. This string then goes through several other functions as specified by the user in the command line arguments.
Each function identifies the substring to redact and does the redaction by overwrting with a block. The redacted files are outputed with the .redacted extension.
 
## Developement Process

- Created redacted.py with the function definifions and function calls in the main loop.
- The file names are taken as input and data from multiple files are sored with a seperator to distinguish the files.
- The functons detect the substrings to redact using spacy, nltk or regex.
- The redacted output is stored in the path given by the user.

__Installation__


1. Clone the repository- git clone https://github.com/CurSpace/cs5293sp22-project1.git
2. Navigate to the project0 folder - cd "cs5293sp22-project1/project1"
3. Install pipenv - pip install pipenv
4. Install the required packages - pipenv install -r requirements.txt
5. Navigate to test folder and run pytest - pipenv run pytest testing_redactor.py


__Python packages used:__

- argparser
- spacy
- nltk
- pytest
- sys
- glob

### Description

- The redactor.py controls the flow of operations.
- The functions are implemted in the redactor.py
- Run the program by:
```
   pipenv run python redactor.py --input [filename] --names --dates --names --phones --genders --address --concept [CONCEPT] --output --stats stderr
```
- the input can be one or more text files
   Ex: 
   
   ```
       pipenv run python redactor.py --input 5.txt 6.txt 7.txt --names --phones --genders --address --concept email --output file --stats stderr
   ```

 
 __Description of User Defined Functions:__
 
 1. input_files(files_in) - takes all the text files and stores them as a single string  with filesep as the seperator between the files.
 
 2. redact_all_names(data) - tokenizes the string using spacy and redacts all names with label PERSON

 3. redact_all_dates(data) - redacts dates using regex

 4. redact_all_phonembers(data) - redacts phone numbers using regex

 5. redact_all_genders(data) - redacts genders uisng a gender list. If the word that incicates gender is present in the gender list, then 
    the gender indicator is redacted.

 6. redact_all_addressess(data) - redacts addressess using regex

 7. redact_all_concepts(data,concept) - redacts entire sentence containing synonym using wordnet

 8. redacted_output(files_in,redacted_file) - stores the redacted text into it's corresponding .redacted file

 9. get_stats(type_of,count) - collects the number of redactions of names,dates,phones,genders,addressess and concepts from the respective 
                        	functioins and appends the result to a global list

 10. write_stats(path,store_stats) - stores the global list returned by write_stats() into the file specified by the user.
    
  
        

    __Sample Output:__
   
 ```
5.redacted

['["Message-ID: <████████.█████████████.JavaMail.evans@thyme> Date: Sun, 25 Nov 2001 20:44:49 -0800 (PST) From: enerfaxdaily@enerfax.com \n███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ Slow browser may need to wait 15 seconds for your email to appear, then scroll to view. mailto:leave-enerfaxdaily-794030K@relay.netatlantic.com to unsubscribe enerfaxdaily as: fermis@ect.enron.com forward to web@enerfax.com  If your email does not support this web version, please subscribe to the free text version by writing subscribe@enerfax.com <mailto:subscribe@enerfax.com> Please visit our website to view today\'s gas and power prices and news by clicking <http://www.enerfax.com>   If you received this in error or no longer wish to subscribe click this link mailto:leave-enerfaxdaily-794030K@relay.netatlantic.com or forward to web@enerfax.com ███ ███ ███ ████  ", \'

6.redacted

['["Message-ID: <████████.█████████████.JavaMail.evans@thyme> Date: Sun, 25 Nov 2001 20:44:49 -0800 (PST) From: enerfaxdaily@enerfax.com \n███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ Slow browser may need to wait 15 seconds for your email to appear, then scroll to view. mailto:leave-enerfaxdaily-794030K@relay.netatlantic.com to unsubscribe enerfaxdaily as: fermis@ect.enron.com forward to web@enerfax.com  If your email does not support this web version, please subscribe to the free text version by writing subscribe@enerfax.com <mailto:subscribe@enerfax.com> Please visit our website to view today\'s gas and power prices and news by clicking <http://www.enerfax.com>   If you received this in error or no longer wish to subscribe click this link mailto:leave-enerfaxdaily-794030K@relay.netatlantic.com or forward to web@enerfax.com ███ ███ ███ ████  ", \'

7.redacted

\', \'Message-ID: <███████.█████████████.JavaMail.evans@thyme> Date: Sat, 26 Nov 0001 00:06:35 -0800 (PST) From: ipayit@enron.com To: frank.ermis@enron.com Subject: Action Requested:  Past Due Invoice for User: FRANK ERMIS Mime-Version: 1.0 Content-Type: text/plain; charset=us-ascii Content-Transfer-Encoding: 7bit X-From: iPayit </O=ENRON/OU=NA/CN=RECIPIENTS/CN=MBX IPAYIT> X-To: Ermis, █████ </O=ENRON/OU=NA/CN=RECIPIENTS/CN=FERMIS> X-cc:  X-bcc:  X-Folder:  ███████████████████ 1 Ermis, ████████████████████: Ermis-F X-FileName: fermis (Non-Privileged).pst  Alert!   You are receiving this message because you have an unresolved invoice in your iPayit in-box that is past due.  It is critical that you login to iPayit and take immediate action to resolve this invoice.   Remember, you play an important role in ensuring that we pay our vendors on time.   Tip!:  You must login to the system to forward this invoice to another user.   To launch iPayit, click on the link below: http://iPayit.enron.com Note:  Your iPayit User ID and Password are your eHRonline/SAP Personnel ID and Password.  First time iPayit user?  For training materials, click on the link below: http://isc.enron.com/site/doclibrary/user/default.asp  Need help? North America: ISC Call Center at ██████████████. Europe: European Accounts Payable at +44-20-7783-7520. \n██████████████████████████████████████████████████████████████████████']

stderr

Names:7
Phones:7
Genders:4
Concepts:3

Note: stats are not mentioned if there are no occurrences.
 ```
__Assumptions__

1. Input files are text files.

2. General regex patterns will be able to find required items.

3. Spacy will find all names with label PERSON.

4. wordnet will accurately redact sentences with specified concept synonyms.

5. Names do not have to be redacted if they appear in emails. 

6. Phonenumbers are of format (713) 345-472.

7. Gender reference are limited to the words mentioned in the gender list.

8. Addressess are of format \d{1,6}\s(?:[A-Za-z0-9#]+\s){0,7}(?:[A-Za-z0-9#]+,)\s*(?:[A-Za-z]+\s){0,3}(?:[A-Za-z]+,)\s*[A-Z]{2}\s*\d{5}

9. wordnet is sufficient to identify synonyms.

10. Output is stored in the locaton specifiec in the user specified locaton with .redacted extension.

11. Stats are stored in the current working directory with the user specifiec file name.
 
__BUGS__

1. The presence of \n interferes with detecting certain ideas like gender. Therefore replacing \n with empty space.

2. Spacy is unable to detect uncommon names like Emris.

3. Redacts wrong 2 numbers at the start of every email ['5941235', '1075855165188', '(713) 345-4727']. CommonRegex is unable to distinguish email identifier and phonenumber.

4. Phones of the format +61-2-9229-2336 are not matched as they are not common north american formats.

5. Redacting concepts interferes with the other options to redact because they have been already redacted, this affects the stats and not all redactions are collected in the stats file.

   


__Testing__

1. test_datainput()

   -> tests if data exists and is not empty

2. test_phonenumbers.py

   -> tests if the lenght of data returned by redact_all_phone_numbers() is greater than zero and makes sure the type of data is not None.

3. test_genders() 

   -> checks if the blocks and the number of redactions are same
   
4. test_names() 
     -> tests if the numbers of blacks is the same as teh number of matched patterns 

5. test_genders() - 
 
    -> checks if the blocks and the number of patterens matched are the same.

 
 

