from django.shortcuts import render
from django.http import StreamingHttpResponse
import requests, os
import subprocess


# Create your views here.
def main(request):
    return render(request, 'main.html')


def video_search(request):
    query = request.GET.get('q')

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
        # Set the video URL
        video_url = 'https://www.youtube.com/watch?v=' + movid

        # Call youtube-dl to download the video as a stream
        cmd = ['youtube-dl', '-o', '-', video_url]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        def stream_response_generator(filelike_object, chunk_size=4096):
            """Generate a Django-style streaming response from a file-like object."""
            while True:
                data = filelike_object.read(chunk_size)
                if not data:
                    break
                yield data

        # Set the response content type to video/mp4
        response = StreamingHttpResponse(
            stream_response_generator(proc.stdout),
            content_type='video/mp4'
        )

        # Set the Content-Length header to the size of the video
        response['Content-Length'] = proc.stdout.tell()

        #return render(request, 'watch.html', {'response': response, 'movid': movid})
        return response

    def disneyplus(request, movid):
        return render(request, 'watch.html')

    def amazonprime(request, movid):
        return render(request, 'watch.html')

    def netflix(request, movid):
        return render(request, 'watch.html')

    # Service Matcher
    if sid == 0:
        return yt_watch(request, movid)
    elif sid == 1:
        return disneyplus(request, movid)
    elif sid == 2:
        return amazonprime(request, movid)
    elif sid == 3:
        return netflix(request, movid)
    else:
        return render(request, 'watch.html', {'status', "No Service ID"})
