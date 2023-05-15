
import subprocess
import logging

log = logging.getLogger(__name__)



def format_output(output: str) -> tuple:
    output = output.split(" ")
    print(output)
    server = output[0].strip(".")
    contact = output[1].strip(".")

    return (server, contact)

def get_SOA(domain: str) -> tuple:
    output = None
    try:
        output = subprocess.check_output(['dig',"soa",domain, '+short'])
        output = str(output, 'utf-8').replace("\n",",").strip(",")
        if 'NXDOMAIN' in output:
            log.error(domain + ",unexpected NX domain error when getting SOA record\n")
        elif(output == ""):
            output = subprocess.check_output(['dig', "soa", "www." + domain, '+short'])
            output = str(output, 'utf-8').replace("\n",",").strip(",")
            return format_output(output)
        elif 'SERVFAIL' in output:
            log.error(domain + ",unexpected SERVFAIL error when getting SOA record\n")
        else:
            return format_output(output)

    except subprocess.CalledProcessError as e:
        log.exception("get SOA had an exception" + domain + "," + str(e) + "\n")
        return output

