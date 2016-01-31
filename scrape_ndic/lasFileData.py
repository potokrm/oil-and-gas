__author__ = 'rpotok'


import urllib2
import pandas as pd
import gc


if __name__ == '__main__':
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    dfScout = pd.read_pickle('')
    dfScout = dfScout[['NDIC File No:', 'lasList']].dropna()
    dfScout['numFiles2'] = dfScout.lasList.apply(lambda x: len(x))
    dfScoutFilt = dfScout[dfScout.numFiles2 > 0]
    prefix = 'https://www.dmr.nd.gov'
    storeData = '/Users/rpotok/Documents/og/LASfiles/NorthDakota/'
    for dfRow in dfScoutFilt.index:
        for las in dfScoutFilt.ix[dfRow].lasList:
            top_level_url = prefix + las
            lasFileName = las.split('/')[-1]
            password_mgr.add_password(None, top_level_url, '', '')
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            ## added try except at 12935
            if '.zip' == top_level_url[-4:]:
                continue
            elif '.lnk' == top_level_url[-4:]:
                continue
            else:
                f = open(storeData + lasFileName, 'w')
                try:
                    data = opener.open(top_level_url)
                    f.write(data.read())
                    data.close()
                except:
                    pass
                f.close()
                #while data.readline():
                #    writeData = data.readline()
                #    f.write(writeData)
                #data.close()
                f.close()
            print dfRow
        gc.collect()



