from django.shortcuts import render
from django.http import StreamingHttpResponse
import requests, os
import subprocess
import youtube_dl


# Create your views here.
def main(request):
    return render(request, 'main.html')


def youtube_search(query):
    # Search for videos on YouTube
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    youtube_url = f'https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&part=snippet&type=video&q={str(query)}'
    youtube_response = requests.get(youtube_url)
    youtube_results = youtube_response.json()['items']

    return youtube_results


def movieaseries_search(query):
    # Search for movies and TV shows on OMDb
    omdb_api_key = os.getenv('OMDB_API_KEY')
    omdb_url = f'http://www.omdbapi.com/?apikey={omdb_api_key}&s={query}&type=movie,series'
    omdb_response = requests.get(omdb_url)
    omdb_results = omdb_response.json()['Search']

    return omdb_results


def video_search(request):
    query = request.GET.get('q')
    youtube_results = youtube_search(query)
    movie_and_series_results = movieaseries_search(query)
    return render(request, 'search.html',
                  {'youtube_results': youtube_results, 'omdb_results': movie_and_series_results, 'query': query})


def watch(request):
    try:
        sid = int(request.GET.get('sid'))
    except:
        sid = False
    try:
        movid = request.GET.get('movid')
    except:
        movid = False

    def yt_watch(request, movid):
        # Construct the URL for the YouTube video
        youtube_url = f'https://www.youtube.com/watch?v={movid}'

        # Start the `youtube-dl` process to download and stream the video
        process = subprocess.Popen(['youtube-dl', '-o', '-', youtube_url], stdout=subprocess.PIPE)

        # Use a generator function to stream the video to the browser in chunks
        def generate():
            while True:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                yield chunk

        # Construct the HTTP response with the generator function as content
        response = StreamingHttpResponse(generate(), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{movid}.mp4"'
        return response

    def disneyplus(request, movid):
        return render(request, 'watch.html')

    def amazonprime(request, movid):
        return render(request, 'watch.html')

    def netflix(request, movid):
        return render(request, 'watch.html')

    # Service Matcher
    if sid == 0:
        yt_watch(request, movid)
    elif sid == 1:
        disneyplus(request, movid)
    elif sid == 2:
        amazonprime(request, movid)
    elif sid == 3:
        netflix(request, movid)
    else:
        return render(request, 'watch.html', {'status', "No Service ID"})
