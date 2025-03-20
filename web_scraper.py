import pandas as pd
import requests
import time
import os

df = pd.read_csv('movies.csv')

OMDB_API_KEY = "a8c3a9e8"  
POSTER_FOLDER = "static/poster" 


os.makedirs(POSTER_FOLDER, exist_ok=True)

def scrape_poster(title, year):
    try:
        
        query = title.replace(' ', '+')
        url = f'http://www.omdbapi.com/?t={query}&y={year}&apikey={OMDB_API_KEY}'
        
        response = requests.get(url)
        data = response.json()

       
        if data.get("Response") == "True" and "Poster" in data:
            image_source = data["Poster"]

            response = requests.get(image_source)
            if response.status_code == 200:
                extension = image_source.split('.')[-1]
                file_name = f'{title.lower().replace(" ", "_")}.{extension}'
                file_path = os.path.join(POSTER_FOLDER, file_name)

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                print(f'[INFO] Poster saved for: {title}')
                return file_name
        
        print(f'[ERROR] No poster found for: {title}')
        return None

    except Exception as e:
        print(f'[ERROR] scraping poster for movie: {title}, error: {e}')
        return None



for index, row in df.iterrows():
    title = row['title']
    release_year = row['release_year']
    poster = row['poster']

    if pd.isna(poster) or poster == '':
        print(f'Searching poster for: {title} ({release_year})...')
        image_title = scrape_poster(title, release_year)

        if image_title:
            df.at[index, 'poster'] = image_title
            df.to_csv('movies.csv', index=False)

        time.sleep(5)  # Pauza da ne bismo preterali sa zahtevima prema API-ju
    else:
        print(f'[INFO] Movie: {title} already has a poster. Skipping.')
