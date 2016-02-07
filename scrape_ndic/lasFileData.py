__author__ = 'rpotok'


import urllib2
import pandas as pd
import gc
import smart_open
import ndic_connect
import json

## code to get LAS files that are linked to the scouting webpage
SOURCE_DATA = "s3://oil-and-gas/scoutData.p"
S3_DIR = "s3://oil-and-gas/LAS-files/"
HTTP_PREFIX = 'https://www.dmr.nd.gov'

## from the scout data I had previously scraped and organized, get
## the dict of ndic_number and LAS file names
def get_ndic_with_las():
    with smart_open.smart_open(SOURCE_DATA) as f:
        temp = fin.read()
        data = pickle.loads(a)
        temp = None
    data['numFiles'] = data.lasList.apply(lambda x: len(x))
    data_filt = data_data.numFiles > 0]
    data_filt = data_filt[['NDIC File No:', 'lasList']].dropna()
    dict_filt = data_filt.set_index('NDIC File No:').to_dict()
    return dict_filt


## open http source
def secure_open()
    password_mgr.add_password(None, top_level_url, ndic_connect.user_name, ndic_connect.passowrd)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    return opener


if __name__ == '__main__':
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    failed_read = []
    las_dict = get_ndic_with_las() 
    ndic_connect = ndic_connect.connect() # get passwords
    for ndic_file_num in las_dict.keys():
        for las in las_dict[ndic_file_num]:
            top_level_url = HTTP_PREFIX + las
            lasFileName = las.split('/')[-1]
            opener = secure_open(ndic_connect)
            ## added try except at 12935, extensions can't read for now
            if  top_level_url[-4:] in  ['.zip','.lnk'] :
                continue
            else:
                ## trade with smart_opoen
                with smart_open.smart_open(S3_DIR + lasFileName, 'w') as f:
                    try:
                        data = opener.open(top_level_url)
                        f.write(data.read())
                        data.close()
                    except:
                        failed_read.append(lasFileName)
                        pass
        gc.collect()
    with smart_open.smart_open(S3_DIR + 'failed_list', 'w') as failed_out:
        json.dump(failed_read)





