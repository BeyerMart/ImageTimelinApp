import streamlit as st
from streamlit_timeline import timeline
import json

import csv
import pandas as pd
import datetime

print("new exec")
def convertMetaRowToJsonMedia(row):
    #input row:
    #Pandas(Index=0, img_id=16058756969, GT=1957, date_taken='1957-01-01 00:00:00', date_granularity=6, url='https://farm8.staticflickr.com/7563/16058756969_81a301a976.jpg', username='Gertrud K.', title='1957', license='All Rights Reserved', license_url=nan)
    #print(row[1])
    id = row[1]
    date_taken = row[3]
    pdDateTaken = pd.to_datetime(date_taken)
    url = row[5]
    caption = row[7]
    credit= row[6]
    headline = caption
    dateGranularity = row[4]
    #media = f"""media": { "url": "{url}", "caption": "Ubahebe Crater", "credit": "h willome" },"""
    #print(media)

    #media = "{ 'media': { 'url': '{url}', 'caption': 'Ubahebe Crater', 'credit': 'h willome' }, 'start_date': { 'year': '1990', 'month': '01', 'day': '02' }, 'text': { 'headline': 'Ubahebe Crater', 'text': 'Date granularity: 6' } }"
    #    event = "{ \"media\": { \"url\": \"{}\", \"caption\": \"{}}\", \"credit\": \"{}}\" }, \"start_date\": { \"year\": \"1990\", \"month\": \"01\", \"day\": \"02\" }, \"text\": { \"headline\": \"{}}\", \"text\": \"Date granularity: {}}\" } }".format(url, caption, credit, headline, dateGranularity)
    event = f"""
        {{
            "media": {{ "url": "{url}", "caption": "{caption}", "credit": "{credit}" }},
            "start_date": {{ "year": "{pdDateTaken.year}", "month": "{pdDateTaken.month}", "day": "{pdDateTaken.day}", "hour": "{pdDateTaken.hour}", "minute": "{pdDateTaken.minute}", "second": "{pdDateTaken.second}" }},
            "text": {{ "headline": "{headline}", "text": "Date granularity: {dateGranularity} <br> ID: {id}" }}
        }}
    """
    #event = f'''{ "media": { "url": "{}", "caption": "{}}", "credit": "{}}" }, "start_date": { "year": "1990", "month": "01", "day": "02" }, "text": { "headline": "{}}", "text": "Date granularity: {}}" } }    '''
    #print(event)
    return event

def parseCSV_DF_dataToJSON(df):
    result = '{ "events": []}'
    #print("dropping first row")
    #df = df.iloc[1:]
    #print(df)
    entries = df.shape[0]
    for data in df.itertuples():
        #print(data.Index)
        #print(data)
        potentialComma = ''
        if data.Index < entries-1:
            potentialComma = ', \n'
        result = result[:-2] + convertMetaRowToJsonMedia(data) + potentialComma + result[-2:]

    #print("result \n" + result)
    return result



def main():
    st.set_page_config(page_title="Timeline Example", layout="wide", )

    
    df = pd.read_csv('meta_shortend.csv')
    #print(df)
    #for image in csvFile['url']:
        #st.image(image)
    # displaying the contents of the CSV file
    #for lines in csvFile:
    #    st.text(lines)

    jsonResult = parseCSV_DF_dataToJSON(df)
    parsed = json.loads(jsonResult)
    print("pretty print")
    print(json.dumps(parsed, indent=4))

    #st.image(csvFile[1])
    #with open('timelineExample.json', "r") as f:
    with open('meta_shortend.json', "r") as f:

        data = f.read()
    timeline(jsonResult, height=800)





if __name__=="__main__":
    main()