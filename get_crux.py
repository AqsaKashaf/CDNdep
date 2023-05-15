# Before run: export GOOGLE_APPLICATION_CREDENTIALS="<path_to_credentials_json>"
# To run: python get_crux.py

from google.cloud import bigquery
import tldextract
from pathlib import Path
import logging
log = logging.getLogger(__name__)
from ca_utils import *

def preprocess_crux(results):
    websites = {}
    for row in results:
        rank = row.rank
        link = row.origin
        domain = get_domain_from_subdomain(link)
        # subdomain = None
        # if link.subdomain != "":
        #     subdomain = f"{link.subdomain}.{domain}"
        if domain not in websites:
            websites[domain] = []
            # websites[domain]["rank"] = []
            # websites[domain]["subdomains"] = []
        websites[domain].append(rank)
        # if subdomain:
        #     websites[domain]["subdomains"].append(subdomain)
    return websites


def query_crux(country, month):
    try:
        client = bigquery.Client()
        query = f"""
            SELECT
                DISTINCT origin,experimental.popularity.rank as rank
            FROM `chrome-ux-report.country_{country}.{month}`
            ORDER BY experimental.popularity.rank ASC
            LIMIT 10000;
        """
        query_job = client.query(query)
        results = query_job.result()  # Waits for job to complete.
        return results
    except Exception as e:
        log.exception(f"Some error happened while querying bigquery for crux dataset, {str(e)}")
        raise Exception(f"Some error happened while querying bigquery for crux dataset, {str(e)}")

def read_crux_file(filename):
    f = open(filename,"r")
    websites = []
    for line in f:
        line = line.strip().split(",")
        websites.append((line[0],line[1]))
    f.close()
    return websites



def extract_crux_file(country, month):
    crux_output_file = f"websites_{country}_{month}"
    my_file = Path(crux_output_file)
    
    if my_file.is_file():
        return read_crux_file(crux_output_file)
    else:
        crux_file_han = open(crux_output_file, "w")
        results = query_crux(country, month)
        crux_websites = preprocess_crux(results)
        websites = []
        for website, details in crux_websites.items():
            rank = min(details)
        # subdomains = ";".join(details["subdomains"])
            crux_file_han.write(f"{rank},{website}\n")
            websites.append((rank,website))

    crux_file_han.close()

    return websites