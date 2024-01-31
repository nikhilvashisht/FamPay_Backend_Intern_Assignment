# FamPay Backend Intern Assignment

API to fetch latest youtube videos using a predefined query. Built with Django, DRF and SQLITE.

## Overview 

The API fetches latest videos from youtube API (with a predefined query, which is 'football' in this case), and saves the data to db. The different fields which are saved to db are : 
- video_id
- video_title
- channel_title
- video_description
- thumbnails_data 

The API serves data in a paginated response, with 10 entries per page.

![image](https://github.com/nikhilvashisht/FamPay_Backend_Intern_Assignment/assets/73426621/38bbbcf0-de61-42de-a08f-579510d3ff3f)


The user can also add their own API Key which can be generated from Google Cloud Console [see here](https://developers.google.com/youtube/v3/getting-started)

![image](https://github.com/nikhilvashisht/FamPay_Backend_Intern_Assignment/assets/73426621/27d4e730-6e34-4881-96ef-1db9c6d1c1a4)


## API Reference 

1. GET ```api/``` : \
    Fetches all stored video data from db and return a JSON response.

2. POST ```api/submit_key``` : \
    Saves the submitted API_KEY to db. This key will be used to access the Youtube API.

    | key | value |
    | ---- | ----- |
    | key | Generated API key |


