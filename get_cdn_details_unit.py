

import sys

from get_soa import *
from get_cname import *
from classification_utils import *
import validators
import json
from cdn_utils import *
import logging
# output: rank,website,provider,providerType,optional

from collections import defaultdict
log = logging.getLogger(__name__)
HAR_DIR="./harfiles"

def find_if_cdn_third(website, cdn, cname, soa_w=None, soa_p=None):

    third = "unknown"
    
    if(match_TLD(website,cname)):
        return "Pvt"

    if("google" in website and "google" in cdn):
       return "Pvt"
    
    if("wix" in website and "wixcdn" in cdn):
        return "Pvt"
    
    if("yahoo" in cdn or "facebook" in cdn):
        return "Pvt"
    
    if("yupoo.com" in website and "upai" in cdn):
        return "Pvt"
    
    if("amazon" in website and "cloudfront" in cdn):
        return "Pvt"
    if(inSAN(website,cname)):
        return "Pvt"

    if(not soa_w): soa_w = get_SOA(website)
    if(not soa_p): soa_p = get_SOA(cname)

    if(not match_SOA(soa_w, soa_p)):
        return "Third"
   
    if(match_TLD_website_SOAprovider(website, soa_p)):
        return "Pvt"
    if(match_loose_TLD(website,cname)):
        return "Pvt"
    
    if(third == "unknown"):
        if("cloudflare" in cdn or "cloudfront" in cdn or "fastly" in cdn or "akamai" in cdn or "azure" in cdn or "google" in cdn or"hinet" in cdn or "gocache" in cdn or "vtex" in cdn or "incapsula" in cdn or "azion" in cdn or "hubspot" in cdn or "edgecast" in cdn or "limelight" in cdn or "alibaba" in cdn or "reflectednetworks" in cdn or "g-core" in cdn or "sitelock" in cdn or "netlify" in cdn or "stackpath" in cdn or "tencent" in cdn or "baishancloud" in cdn or "edgecdnru" in cdn):
            return "Third"
  
    return third     

def read_resources(website, harfiles_path):
    website_resources = set()
  
    harf = open(f"{harfiles_path}/{website}.har","r")
    try:
        text = json.loads(harf.read())
        all_urls = text["log"]["entries"]
        website_resources.add("www."+website)
        for url in all_urls:
            rsrc = url["request"]["url"]
            rsrc_domain = get_hostname_from_url(rsrc)
            website_resources.add(rsrc_domain)
    except Exception as e:
        log.exception(f"something happened while reading resources for {website}, {str(e)}")
    harf.close()
    return website_resources


def get_har(website, HAR_DIR):
    output = run_subprocess(["node","get_har.js",website, HAR_DIR])
    if(output == -1):
        raise Exception("Could not get har file")

def get_internal_resources(website,links):
    
    internals = set()
    for link in links:
        link_domain = get_domain_from_subdomain(link)
        if(match_loose_TLD(website,link_domain)):
            internals.add(link)
        elif(inSAN(website,link_domain)):
            internals.add(link)
        elif("reddit" in website and "reddit" in link):
            internals.add(link)

    return internals

def match_CDN_cname(cdn_lib, cname):
    for cname_cdn,cdn in cdn_lib.items():
        if(cname_cdn in cname):
            return cdn
    return None

def find_CDN(internal_links, CDN_MAP):
    cdns = defaultdict(list)
    for link in internal_links:
        matched_cdn = match_CDN_cname(CDN_MAP,link)
        if(matched_cdn):
            cdns[matched_cdn].append(link)
            print(matched_cdn, link)
        cnames_link = get_cname(link)
        print("cnames", cnames_link)
        for cname in cnames_link:
            matched_cdn = match_CDN_cname(CDN_MAP,cname)
            if(matched_cdn):
                cdns[matched_cdn].append(cname)
    return cdns

def get_CDN_details(host: str, CDN_MAP: dict) -> dict :
   
    if(validators.url(host)):
        host = get_hostname_from_url(host)
    
    valid_input = check_if_valid(host)
   
    if(valid_input):
        get_har(host,HAR_DIR)
        resources = read_resources(host, HAR_DIR)
        # remove_file(f"{HAR_DIR}/{host}.har")
        internal_resources = get_internal_resources(host, resources)
        print(resources,internal_resources)
        cdns = find_CDN(internal_resources, CDN_MAP)
        print(cdns)
        return cdns

    else:
        raise Exception("Invalid input")


def classify(website, providers, cnames):

    
    output = "unknown"
    for p in providers:
        output = find_if_cdn_third(website, p, cnames)
        if(output != "unknown"):
            break
    
    return output

def main():
    # check if input given
    
    if(len(sys.argv) < 2):
        raise Exception("\nPlease provide a website name to get its certificate authority details.\n")
    
    
    host = sys.argv[1]
    CDN_MAP = read_CDN_MAP()
    print(find_and_classify(host, CDN_MAP))
    # print(host, details["ocsp"], output)
    

def find_and_classify(host: str, CDN_MAP: dict) -> tuple:
    details = get_CDN_details(host, CDN_MAP)
    print(details)
    result = {}
    for cdn,cnames in details.items():
        output = classify(host, cdn, cnames)
        print(output, cdn, cnames)
        exit()
        if((host,cdn) in result):
            if(result[(host,cdn)] != output):
                if(result[(host,cdn)] == "unknown"):
                    result[(host,cdn)] = output
                elif(output == "Third"):
                    result = output
        else:
            result[(host,cdn)] = output
    
    
    return result

if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig('log.conf')
    main()
