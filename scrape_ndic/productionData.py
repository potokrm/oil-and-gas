__author__ = 'rpotok'

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


if __name__ == '__main__':
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    dfScout = pd.read_pickle('')
    dfScoutFilt = dfScout[dfScout.prodLink.notnull()]
    dfScoutFilt = dfScoutFilt[dfScoutFilt.index >= 2000]
    prefix = 'https://www.dmr.nd.gov/oilgas/feeservices/'
    top_level_url = prefix + dfScoutFilt.iloc[0].prodLink
    password_mgr.add_password(None, top_level_url, '', '')
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    pandasList = []
    for elem in dfScoutFilt.index:
        print elem
        listOfTitles = []
        prodSuffix = dfScoutFilt.ix[elem].prodLink
        url = prefix + prodSuffix
        data = opener.open(url)
        datalines = data.read()
        data.close()
        if len(datalines.split('Monthly Production Data')) < 2:
            print 'not enough for table split %s' % url
            continue
        table = datalines.split('Monthly Production Data')[2]
        tableSplitList = table.split('<td style="border:1px solid saddlebrown;"')
        if len(tableSplitList) < 2:
            print 'table split went poorly %s' % url
            continue
        for tableRow, element in enumerate(tableSplitList):
            if tableRow == 0:
                titleList = element.split('title="')
                for titleNum, title in enumerate(titleList):
                    if titleNum > 0:
                        listOfTitles.append(title.split('"')[0])
                listOfTitles.append('Element')
                listOfTitles.append('index_val')
                pdList = []
                pdRow = []
            elif np.floor(float(tableRow)/(len(listOfTitles)-2)) == float(tableRow)/(len(listOfTitles)-2):
                dataExtract = element.split(">")[1].split("<")[0]
                pdRow.append(dataExtract)
                pdRow.append(dfScoutFilt.ix[elem]['webCallElem'])
                pdRow.append(elem)
                pdList.append(pdRow)
                pdRow = []
            else:
                dataExtract = element.split(">")[1].split("<")[0]
                pdRow.append(dataExtract)
        df = pd.DataFrame(pdList, columns = listOfTitles)
        pandasList.append(df)

    dfConcat = pd.concat(pandasList)
    dfConcat.to_pickle('/Users/rpotok/Documents/personal/scrape/prodData2000_up.p')
        #soup = BeautifulSoup(datalines)
        #except:
        #    print 'bad link %s' % url
        #    pass
        #print elem
        #break


