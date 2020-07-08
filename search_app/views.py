import requests
from django.conf import settings
from django.shortcuts import render, redirect
from isodate import parse_duration

def index(request):
    videos = []
    if request.method == "POST":

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        videoIds = []
        for result in results:
            videoIds.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ videoIds[0] }')

        video_params = {
            'part' : 'snippet,contentDetails',
            'key' : settings.YOUTUBE_API_KEY,
            'id' : ','.join(videoIds),
            'maxResults' : 9,
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"]}',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }

    return render(request, 'search_app/index.html', context)
