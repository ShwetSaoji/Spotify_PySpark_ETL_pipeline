import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbLRQDuF5jeBp"
    playlist_URI = playlist_link.split("/")[-1]
    spotify_data = sp.playlist_tracks(playlist_URI)
    
    print(spotify_data)
    
    cilent = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    cilent.put_object(
        Bucket="spotify-etl-project-shwet",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(spotify_data)
        )

    glue = boto.client("glue")
    gluejobname = "spotify_transformation_job"
    
    try:
        runId = glue.start_job_run(JobName=gluejobname)
        status = glue.get_job_run(JobName=gluejobname, RunId = runId["JobRunId"])
        print("Job Status :" , status['JobRun']['JobRunState'])
    except exception as e:
        print(e)
