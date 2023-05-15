import sys
from get_crux import *
from get_cdn_details_unit import *





def main():
    # check if input given
    country = "us"
    if(len(sys.argv) > 1):
        country = sys.argv[1]
        if(not check_valid_country(country)):
            raise Exception("Please enter a valid country code, {country} is not valid")
    
    month = get_last_month()
    
    
    websites = extract_crux_file(country, month)
    CDN_MAP = read_CDN_MAP()
    results = {}
    count = 0
    for r,w in websites:
        output = find_and_classify(w, CDN_MAP)
        print(output)
        results[(r,w)] = output
        count+=1
        if(count == 5):
            print(country,"cdn",month,results)
            write_results(country,"cdn",month,results)
            results = {}
            count = 0
            exit()


        

if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig('log.conf')
    main()