#Utility constants and functions for multisurf
#lengths are in bytes

#Protocol constants
PREAMBLE_LEN = 7
PREAMBLE = "GET OMB"

URL_LEN = 10
RESP_BODY_LEN = 15

# Server response codes
RESP_CODE_LEN = 1
ERR_CODE = "0"
SUCCESS_CODE = "1"

#split a url into its host and path portions
def split_url(url):
    split = []
    if('/' in url):
        split = url.split('/',1)
        split[1] = '/'+split[1]
    else:
        split = [url, ""]
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
        
    
