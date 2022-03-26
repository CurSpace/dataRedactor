import argparse
import redactor


if __name__ == "__main__":
    

    arguments = argparse.ArgumentParser()
    arguments.add_argument("--input",type = str, required = True, help = "path to input files", nargs = "*", action = "append" )
    arguments.add_argument("--names", required = False, help = "option to redate names", action = "store_true")
    arguments.add_argument("--genders", required = False, help = "option to redact genders", action = "store_true")
    arguments.add_argument("--dates", required = False, help = "option to redact dates", action = "store_true")
    arguments.add_argument("--phones", required = False, help = "option to redact phone numbers", action = "store_true")
    arguments.add_argument("--phones", required = False, help = "option to redact phone numbers", action = "store_true")
    # can be repeated multiple times
    arguments.add_argument("--concept", type = str, required = False, help = "option to redact concepts", nargs= "*", action = "append")
    arguments.add_argument("--stats", type = str, required = False, help = "option to to print stats for redactions")
    arguments.add_argument("--output", type = str, required = True, help = "path  to outputfile")

    args = arguments.parse_args()
    data  = redactor.input_files(args.input)

    if args.names:
        data = redactor.redact__all_names(data)
    
    if args.dates:
        data = redactor.redact_all_dates(data)
    
    if args.phones:
        data = redactor.redact_all_phonenumbers(data)
        

    if args.genders:
        data = redactor.redact_all_genders(data)

    if args.concept:
        data = redactor.redact_all_concepts(data, args.concept)
        
    if args.output:
        redactor.get_output(args.input, data, args.output)

    if args.stats:
        
        redactor.write_stats()






