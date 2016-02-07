__author__ = 'rpotok'

import urllib2
from bs4 import BeautifulSoup
import pandas as pd

## write a function to scrape each of these from the scout webpage:
## NDIC File No
## API Number
## County
## Status Date
## Wellbore type
## Latitude
## Longitude
## Total depth
## list of las files
## production file

S3_DIR = "s3://oil-and-gas/scout-data/"

param_list = ['NDIC File No:', 'API No:', 'Status Date:', 'Wellbore type:',
            'Latitude:', 'Longitude:', 'Current Operator:', 'Total Depth:',
            'Perfs:', 'Cum Oil:', 'Cum MCF Gas:', 'Cum Water:']


def get_bold_param(param, data):
    splitOnParam = data.split(param)
    if len(splitOnParam) > 1:
        output = splitOnParam[1].split('<b>')[1].split('</b>')[0]
        return output
    else:
        return None

## open http source
def secure_open(password_mgr, top_level_url)
    password_mgr.add_password(None, top_level_url, ndic_connect.user_name, ndic_connect.passowrd)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    return opener

def get_data(ndic):
    w = 'https://www.dmr.nd.gov/oilgas/feeservices/getscoutticket.asp?FileNumber=%s' % ndic
    data = opener.open(w)
    datalines = data.read()
    data.close()
    for Parameter in param_list:
        ## get all of the params in param_list
        inList.append(get_bold_param(Parameter, datalines))
    soup = BeautifulSoup(datalines)
    laslinks = []
    prod = ''
    ## get production and las file links as well
    for link in soup.find_all('a'):
        href = link.get('href')
        if '.las' in href:
            laslinks.append(href)
        elif 'getwellprod' in href:
            prod = href
    inList.append(laslinks)
    if len(prod)>0:
        inList.append(prod)
    else:
        inList.append(None)
    return inList


if __name__ == '__main__':
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    ## need to open the website with the login page once
    top_level_url = 'https://www.dmr.nd.gov/oilgas/feeservices/getscoutticket.asp?FileNumber=15322'
    opener = secure_open(password_mgr, top_level_url)
    dfList = []
    for elem in range(1, 25853):  ## manually looked up that the last well index was 25853
        inList = []
        try:
            ## get a list of data from the scout data, one row per well
            in_list = get_data(elem)
        except:
            in_list = [None]*14
        in_list.append(elem)
        if len(in_list) != 15: ## check that we extracted all the data (should be 15 cols)
            print 'wrong column count at NDIC %s' % elem
        df_list.append(in_list)
    ## need to append the extra columns we added
    dfCols = paramList + ['las_list', 'prod_link', 'web_call_elem']
    df = pd.DataFrame(df_list, columns = dfCols)
    df['num_files'] = df.lasList.apply(lambda x: len(x))
    with smart_open.smart_open(S3_DIR + 'scout_data.p', 'wb') as fout:
        pickle.dump(df. fout)



