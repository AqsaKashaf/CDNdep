import sys
from get_crux import *
from get_cdn_details_unit import *





def main():
    # check if input given
    country = "us"
    if(len(sys.argv) < 2):
        raise Exception("Please provide an output file path")
    
    output_file_path = sys.argv[1]
    if(len(sys.argv) > 2):
        country = sys.argv[2]
        if(not check_valid_country(country)):
            raise Exception("Please enter a valid country code, {country} is not valid")
    
    month = get_last_month()
    websites = extract_crux_file(country, month)
    CDN_MAP = read_CDN_MAP()
    results = {}
    count = 0
    for r,w in websites:
        output = find_and_classify(w, CDN_MAP)
        results[(r,w)] = output
        count+=1
        if(count == 5):
            print(country,"cdn",month,results)
            write_results(output_file_path,country,"cdn",month,results)
            results = {}
            count = 0
            exit()


        

if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig('log.conf')
    main()