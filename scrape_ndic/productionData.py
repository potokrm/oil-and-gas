__author__ = 'rpotok'

import urllib2
import pandas as pd
import numpy as 
import smart_open
import ndic_connect
import json
import pickle

## create a large table of production data and north dakota wells

## code to get oil production files that are linked to the scouting webpage

## need to fix, put a dictionary in and pass both items to record the ndic number as well
SOURCE_DATA = "s3://oil-and-gas/scout.p"
S3_DIR = "s3://oil-and-gas/production-data/"
HTTP_PREFIX = 'https://www.dmr.nd.gov/oilgas/feeservices/'

## return dictionary of well numbers and links
def get_ndic_with_production_data():
    with smart_open.smart_open(SOURCE_DATA) as f:
        temp = fin.read()
        data = pickle.loads(a)
        temp = None
    data_filt = data[data.prodLink.notnull()])
    all_links = data_filt[['prodLink', 'NDIC']].set_index('NDIC').to_dict()
    return data_filt

## open http source
def secure_open(password_mgr, top_level_url)
    password_mgr.add_password(None, top_level_url, ndic_connect.user_name, ndic_connect.passowrd)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    return opener


def get_prod_url_data(url, opener):
    data = opener.open(url)
    datalines = data.read()
    data.close()
    return datalines


## took trial and error to get this right
def table_splitter(tableData):
    for tableRow, element in enumerate(tableSplitList):
        ## special case for first row, set the column names
        if tableRow == 0:
            titleList = element.split('title="')
            for titleNum, title in enumerate(titleList):
                if titleNum > 0:
                    listOfTitles.append(title.split('"')[0])
            listOfTitles.append('Element')
            listOfTitles.append('index_val')
            pdList = []
            pdRow = []
        ## normal row
        elif np.floor(float(tableRow)/(len(listOfTitles)-2)) == float(tableRow)/(len(listOfTitles)-2):
            dataExtract = element.split(">")[1].split("<")[0]
            pdRow.append(dataExtract)
            pdRow.append(elem)
            pdList.append(pdRow)
            pdRow = []
        else:
            dataExtract = element.split(">")[1].split("<")[0]
            pdRow.append(dataExtract)
    return pdList, column_list


def split_html_table(datalines)
    listOfTitles = []
    if len(datalines.split('Monthly Production Data')) < 2:
        print 'not enough for table split %s' % url
        return url
    table = datalines.split('Monthly Production Data')[2]
    tableSplitList = table.split('<td style="border:1px solid saddlebrown;"')
    if len(tableSplitList) < 2:
        print 'table split went poorly %s' % url
        return url
    pdList, column_list = table_splitter(tableData)

    list_of_titles += ['NDIC Index']
    df = pd.DataFrame(pdList, columns = listOfTitles)
    return df


if __name__ == '__main__':
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    top_level_url = prefix + dfScoutFilt.iloc[0].prodLink
    opener = secure_open(password_mgr, top_level_url)
    all_links = get_ndic_with_production_data()
    pandas_list = []  ## append dataframes to a list, then concat list for big prod table
    for production_link in all_links.keys():   
        try:
            datalines = get_prod_url_data(HTTP_PREFIX + production_link, opener)
            temp_df, column_names = split_html_table(datalines)
            pandas_list.append(temp_df, column_names)
        except:
            raise 
    dfConcat = pd.concat(pandasList)
    with smart_open.smart_open(S3_DIR + 'production_data.p', 'wb') as fout:
        pickle.dump(dfConcat. fout)



