

import tldextract


def match_TLD_website_SOAprovider(website: str, soa_p: tuple) -> bool:
    match = False
 
    soa_provider_server = soa_p[0]
    soa_provider_contact = soa_p[1]

    if(website == soa_provider_server):
        match = True
    elif(website == soa_provider_contact):
        match = True
    return match

def match_SOA(soa_w: tuple, soa_p: tuple) -> bool:
    match = True
    
   
    soa_website_server = soa_w[0]
    soa_provider_server = soa_w[0]

    soa_website_contact = soa_p[1]
    soa_provider_contact = soa_p[1]

    if(soa_website_server != soa_provider_server):
        match = False
    if(soa_website_contact != soa_provider_contact):
        match = False

    return match


def match_loose_TLD(website,provider):
    w_sld = tldextract.extract(website).domain
    provider_sld = tldextract.extract(provider).domain
    
    if(w_sld == provider_sld):
        return True
    

def match_TLD(website,provider):
   
    if(website.lower() == provider.lower()):
        return True
    

