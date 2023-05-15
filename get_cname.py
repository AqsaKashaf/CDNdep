
import subprocess
import logging
from cdn_utils import *

log = logging.getLogger(__name__)



def format_output(output: str) -> tuple:
    output = output.split(",")
    result = []
    for i in output:
        if(not isIP(i)):
            result.append(i.strip("."))
    

    return result

def get_cname(domain: str) -> tuple:
    output = None
    try:
        output = subprocess.check_output(['dig',domain, '+short'])
        output = str(output, 'utf-8').replace("\n",",").strip(",")
        if 'NXDOMAIN' in output:
            log.error(domain + ",unexpected NX domain error when getting SOA record\n")
        elif(output == ""):
            output = subprocess.check_output(['dig',"www." + domain, '+short'])
            output = str(output, 'utf-8').replace("\n",",").strip(",")
            return format_output(output)
        elif 'SERVFAIL' in output:
            log.error(domain + ",unexpected SERVFAIL error when getting SOA record\n")
        else:
            return format_output(output)

    except subprocess.CalledProcessError as e:
        log.exception("get_cname resulted in an exception" + domain + "," + str(e.output) + "\n")
        return output

