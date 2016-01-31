__author__ = 'rpotok'

import urllib2
from bs4 import BeautifulSoup
import pandas as pd

## do a get method for each of these:
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


def get_bold_param(param, data):
    splitOnParam = data.split(param)
    if len(splitOnParam) > 1:
        output = splitOnParam[1].split('<b>')[1].split('</b>')[0]
        return output
    else:
        return None


if __name__ == '__main__':
    elem_start = 10000
    elem_end = 25500
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    top_level_url = 'https://www.dmr.nd.gov/oilgas/feeservices/getscoutticket.asp?FileNumber=15322'
    t2 = 'https://www.dmr.nd.gov/oilgas/feeservices/getscoutticket.asp?FileNumber=15323'
    password_mgr.add_password(None, top_level_url, '', '')
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)

    paramList = ['NDIC File No:', 'API No:', 'Status Date:', 'Wellbore type:',
                 'Latitude:', 'Longitude:', 'Current Operator:', 'Total Depth:',
                 'Perfs:', 'Cum Oil:', 'Cum MCF Gas:', 'Cum Water:']
    dfList = []
    for elem in range(elem_start, elem_end):
        inList = []
        w = 'https://www.dmr.nd.gov/oilgas/feeservices/getscoutticket.asp?FileNumber=%s' % elem
        try:
            data = opener.open(w)
            datalines = data.read()
            data.close()
            for Parameter in paramList:
                inList.append(get_bold_param(Parameter, datalines))
            soup = BeautifulSoup(datalines)
            laslinks = []
            prod = ''
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
        except:
            inList = [None]*14
        inList.append(elem)
        if len(inList) != 15:
            print 'wrong count as %s' % elem
        dfList.append(inList)
        print elem
        #break
    dfCols = paramList + ['lasList', 'prodLink', 'webCallElem']
    df = pd.DataFrame(dfList, columns = dfCols)
    df['num_files'] = df.lasList.apply(lambda x: len(x))
    df.to_pickle('/Users/rpotok/Documents/personal/scrape/scoutData%s_%s.p' % (elem_start, elem_end))



