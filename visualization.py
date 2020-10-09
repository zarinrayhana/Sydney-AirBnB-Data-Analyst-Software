import wx
import wx.grid
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import json
from numpy.core.defchararray import lower

# LOAD THE FILES NEEDED
listings = pd.read_csv('./csvs/listings_dec18.csv')
reviews = pd.read_csv('./csvs/reviews_dec18.csv')

# GLOBAL VARIABLES
# STORE ONLY THE NEEDED COLUMNS INTO NEW DATAFRAMES
listingsReducedColumns = listings[
    [
        'id',
        'name',
        'host_name',
        'host_since',
        'street',
        'neighbourhood',
        'neighbourhood_cleansed',
        'property_type',
        'room_type',
        'amenities',
        'price',
        'review_scores_rating'
    ]
]
commentsReducedColumns = reviews[['listing_id', 'comments']]
cleanlinessKeywords = ['clean', 'neat', 'fresh', 'hygienic', 'taintless', 'sterile', 'sanitary', 'washed', 'flawless', 'bright', 'shiny', 'sparkling']

# FUNCTIONS TO RETRIEVE LISTINGS BASED ON USER INPUTS
def showListings(listingToDisplay):
    cols = listingToDisplay[0] #len = 13
    rows = len(listingToDisplay)

    df = pd.DataFrame(listingToDisplay[1:], columns=cols)
    # print(df.shape)
    # print(df)
    result = df.to_json(orient='index')
    #print(result)

    #WRITES THE CONVERTED JSON DATAFRAME TO A FILE SO IT CAN BE USED IN THE GUI MODULE
    with open('listings.json', 'w') as jsonListings:
        json.dump(result, jsonListings)

def findKeyword(startperiod, endperiod, keyword):
    # MANIPULATE THE PROVIDED DATE ARGUMENTS
    splitStartPeriod = startperiod.split('/')
    splitEndPeriod = endperiod.split('/')
    startDate = datetime.datetime(int(splitStartPeriod[-1]), int(splitStartPeriod[-2]), int(splitStartPeriod[-3]))
    endDate = datetime.datetime(int(splitEndPeriod[-1]), int(splitEndPeriod[-2]), int(splitEndPeriod[-3]))

    listingsReducedColumns.amenities = listingsReducedColumns.amenities.apply(lower)
    # FILTER THE LISTINGS TO ONES THAT CONTAIN THE PROVIDED KEYWORD
    # A NEW COLUMN IS CREATED TO STORE WHETHER IF THE LISTING'S A MATCH WITH THE KEYWORD
    listingsReducedColumns['matchedAmenities'] = listingsReducedColumns.amenities.apply(lambda row: 'match' if keyword in row else 'no match')

    # CONVERT THE HOST_SINCE TYPE INTO DATETIME AND STORE IN A NEW COLUMN
    listingsReducedColumns['period'] = pd.to_datetime(listingsReducedColumns.host_since)

    # THE LISTING ROWS MATCHING THE PROVIDED KEYWORD IS STORED IN THE 'MATCHED' VARIABLE
    matched = listingsReducedColumns[
        (listingsReducedColumns.matchedAmenities == 'match') &
        (listingsReducedColumns.period >= startDate) &
        (listingsReducedColumns.period <= endDate)
    ]
    matchedListingsIDs = list(matched.id)
    print('listings matched with {}'.format(keyword))
    # print(matched)
    # print(matchedListingsIDs)

    # RETURNS A DICTIONARY WITH THE KEYWORD AS KEY AND MATCHING LISTINGS AS THE VALUE (IN A LIST)
    return {keyword: matchedListingsIDs}

# findKeyword('1/1/2009', '30/6/2009', 'elevator')

def getListings(startperiod, endperiod, suburbName='sydney', keyword=None):
    # MANIPULATE THE PROVIDED DATE ARGUMENTS
    splitStartPeriod = startperiod.split('/')
    splitEndPeriod = endperiod.split('/')
    startDate = datetime.datetime(int(splitStartPeriod[-1]), int(splitStartPeriod[-2]), int(splitStartPeriod[-3]))
    endDate = datetime.datetime(int(splitEndPeriod[-1]), int(splitEndPeriod[-2]), int(splitEndPeriod[-3]))

    # INITIALIZE THE DICTIONARY FOR IF A KEYWORD IS PROVIDED, AND THE LIST TO SEND TO SHOWLISTINGS FUNCTION
    filteredListings = {}
    result = []
    # CONVERT THE STRINGS, KEYWORD AND SUBURBNAME INTO LOWERCASE
    suburbName = suburbName.lower()
    listingsReducedColumns.street = listingsReducedColumns.street.apply(lower)
    listingsReducedColumns.neighbourhood_cleansed = listingsReducedColumns.neighbourhood_cleansed.apply(lower)

    if keyword != None:
        keyword = keyword.lower()
        filteredListings = findKeyword(startperiod, endperiod, keyword)
        # CHECK IF ANY MATCH FOUND
        if len(filteredListings[keyword]):
            print('Properties matching the provided keyword found')
            # RENAMES THE COLUMN MATCHEDAMENITIES INTO ANOTHER NAME INSTEAD OF ADDING A NEW COLUMN, TO BE USED TO MATCH SUBURBNAME
            listingsReducedColumns.rename(columns={'matchedAmenities': 'matchedSuburb'}, inplace=True)

            # COMPARE THE RETURNED LISTING IDS AND SAVE THE BOOLEAN RESULT IN A NEW COLUMN
            listingsReducedColumns['matchedSuburb'] = listingsReducedColumns.id.apply(lambda row: 'match' if int(row) in filteredListings[keyword] else 'no match')

            # THE LISTINGS THAT MATCHES THE LISTING IDS AND HAVE SUBURBNAME AS EITHER STREET NAME OR NEIGHBOURHOOD NAME
            matched = listingsReducedColumns[
                ((listingsReducedColumns.matchedSuburb == 'match') &
                (listingsReducedColumns.street == suburbName)) |
                ((listingsReducedColumns.matchedSuburb == 'match') &
                (listingsReducedColumns.neighbourhood_cleansed == suburbName)) |
                ((listingsReducedColumns.matchedSuburb == 'match') &
                (listingsReducedColumns.neighbourhood == suburbName))
            ]
            result = [matched.columns.values.tolist()] + matched.values.tolist()
        else:
            return 'No match found'

    else:
        listingsReducedColumns['period'] = pd.to_datetime(listingsReducedColumns.host_since)
        matched = listingsReducedColumns[
            ((listingsReducedColumns.period >= startDate) & (listingsReducedColumns.period <= endDate)) &
            ((listingsReducedColumns.street == suburbName) |
             (listingsReducedColumns.neighbourhood_cleansed == suburbName) |
             (listings.neighbourhood == suburbName)
             )
        ]
        print(matched)
        result = [matched.columns.values.tolist()] + matched.values.tolist()

    return showListings(result)

# getListings('1/1/2015', '30/12/2019')

def showPriceDist(startperiod, endperiod):
    # MANIPULATE THE PROVIDED DATE ARGUMENTS
    splitStartPeriod = startperiod.split('/')
    splitEndPeriod = endperiod.split('/')
    startDate = datetime.datetime(int(splitStartPeriod[-1]), int(splitStartPeriod[-2]), int(splitStartPeriod[-3]))
    endDate = datetime.datetime(int(splitEndPeriod[-1]), int(splitEndPeriod[-2]), int(splitEndPeriod[-3]))

    # CONVERT THE HOST_SINCE STRINGS INTO DATETIME TYPE
    listingsReducedColumns['period'] = pd.to_datetime(listingsReducedColumns.host_since)
    # CAST THE STRINGS IN PRICE COLUMN AS FLOAT
    listingsReducedColumns['price'] = listingsReducedColumns.price.apply(lambda x: float(x.replace('$', '').replace(',', '')) if isinstance(x, str) else float(x))

    # RETURN ONLY RECORDS IN THE PROVIDED PERIODS
    result = listingsReducedColumns[(listingsReducedColumns.period >= startDate) & (listingsReducedColumns.period <= endDate)]
    # print(result)
    years = result.period.dt.year.unique()
    priceDist = {}
    for year in years:
        yearPrice = result[result.period.dt.year == year]
        priceDist[year] = [yearPrice.price]
        plt.hist(priceDist[year], range=(0, 3000), bins=150, alpha=0.5, density=True)

    plt.legend([year for year in years])
    plt.show()
    return priceDist

# showPriceDist('1/1/2015', '30/12/2019')

def showPopularListings(startperiod, endperiod, suburbName='sydney'):
    # MANIPULATE THE PROVIDED DATE ARGUMENTS
    splitStartPeriod = startperiod.split('/')
    splitEndPeriod = endperiod.split('/')
    startDate = datetime.datetime(int(splitStartPeriod[-1]), int(splitStartPeriod[-2]), int(splitStartPeriod[-3]))
    endDate = datetime.datetime(int(splitEndPeriod[-1]), int(splitEndPeriod[-2]), int(splitEndPeriod[-3]))

    # INITIALIZE THE DICTIONARY FOR IF A KEYWORD IS PROVIDED, AND THE LIST TO SEND TO SHOWLISTINGS FUNCTION
    filteredListings = {}

    # CONVERT THE HOST_SINCE STRINGS INTO DATETIME TYPE
    listingsReducedColumns['period'] = pd.to_datetime(listingsReducedColumns.host_since)
    # CONVERT THE STRINGS, KEYWORD AND SUBURBNAME INTO LOWERCASE
    suburbName = suburbName.lower()
    listingsReducedColumns.street = listingsReducedColumns.street.apply(lower)
    listingsReducedColumns.neighbourhood_cleansed = listingsReducedColumns.neighbourhood_cleansed.apply(lower)

    # SORT THE REVIEW_SCORES_RATING COLUMN IN DESCENDING ORDER
    listingsReducedColumns.sort_values(by='review_scores_rating', inplace=True, ascending=False)

    matched = listingsReducedColumns[
        ((listingsReducedColumns.period >= startDate) & (listingsReducedColumns.period <= endDate)) &
        ((listingsReducedColumns.street == suburbName) |
         (listingsReducedColumns.neighbourhood_cleansed == suburbName) | (listingsReducedColumns.neighbourhood == suburbName))
    ]

    # CONVERT THE VALUES INTO A LIST
    allRecords = matched.values.tolist()
    # SELECTS THE FIRST 5 VALUES
    top5 = allRecords[:5]

    # STORES THE TOP 5 VALUES AND COLUMN NAMES TO A LIST
    # AND WRITE THE LIST INTO A JSON FILE TO DISPLAY ON THE GUI LATER
    result = [matched.columns.values.tolist()] + allRecords

    df = pd.DataFrame(result[1:5], columns=result[0])
    jsonResult = df.to_json(orient='index')
    
    with open('popularListings.json', 'w') as jsonListings:
        json.dump(jsonResult, jsonListings)
        
    # STORE THE VALUES INTO THE DICTIONARY WITH SUBURBNAME AS ITS KEY
    filteredListings[suburbName] = top5

    return filteredListings

# showPopularListings('1/1/2018', '31/1/2018', suburbName='waverley')

def showCleanComments():
    cleanCommentTotal = 0
    cleanlinessKeywordDict = {}
    print(reviews)

    allCommentStr = reviews.comments.values.tolist()
    print(type(allCommentStr))
    print(allCommentStr)
    totalCommentList = int(len(allCommentStr))

    for kw in cleanlinessKeywords:
        for i in range(totalCommentList):
            if kw in allCommentStr[i] and kw not in (cleanlinessKeywordDict.keys()):
                cleanCommentTotal += 1
                cleanlinessKeywordDict[kw] = 1
            elif kw in allCommentStr[i] and kw in (cleanlinessKeywordDict.keys()):
                cleanCommentTotal += 1
                prevCount = cleanlinessKeywordDict[kw]
                cleanlinessKeywordDict[kw] = prevCount + 1

    # print(cleanlinessKeywordDict)
    return cleanlinessKeywordDict


    # reviews['comments'] = reviews.comments.apply(lambda row: for kw in cleanlinessKeywords)

showCleanComments()
