#Utility constants and functions for multisurf
#define the number of peers
NUM_PEERS = 1

#lengths are in bytes
#Protocol constants
PREAMBLE_LEN = 7
PREAMBLE = "GET OMB"

#Lengths in bytes of the length values
URL_LEN = 10
REQ_LEN = 10
RESP_BODY_LEN = 15

# Server response codes
RESP_CODE_LEN = 1
ERR_CODE = "0"
SUCCESS_CODE = "1"

#Client result
PEER_ERR = 0
NOT_IDENTICAL_ERR = 1
IDENTICAL = 2

# headers for version 0 HTTP requests
user_agent_hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0'
accept_hdr = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
accept_lang_hdr = 'en-US,en;q=0.5'
cookie_hdr =  'Marcela'
conn_hdr = 'keep-alive'

#split a url into its host and path portions
def split_url(url):
    split = []
    if('/' in url):
        split = url.split('/',1)
        split[1] = '/'+split[1]
    else:
        split = [url, "/"]
    return split

#pad the length of the url up to URL_LEN
def pad_length(length,isRespBody=False):
    paddingLen = URL_LEN

    if isRespBody == True:
        paddingLen = RESP_BODY_LEN

    padded = str(length)
    while len(padded) < paddingLen:
        padded = '0'+padded
    return padded
        
    
