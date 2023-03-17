from django.shortcuts import render, redirect
from googleapiclient.discovery import build
import os
from urllib.parse import urlparse
from .models import Click


# Create your views here.
def search(request):
    api_key = os.getenv("google_api_key")
    cse_id = os.getenv("google_cse_id")
    num_results = 10

    results = []

    if request.GET.get('q'):
        query = request.GET.get('q')

        service = build('customsearch', 'v1', developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()

        items = res.get('items', [])

        for item in items:
            title = item['title']
            link = item['link']
            snippet = item.get('snippet', '')
            parsed_link = urlparse(link)
            uri = parsed_link.path
            domain = urlparse(link).netloc
            click = Click.objects.filter(url=domain).order_by('-id').first()
            click_count = click.click_count if click else 0
            results.append(
                {'title': title, 'link': link, 'snippet': str(snippet), 'domain': domain + uri, 'click_count': click_count})
        return render(request, 'search.html', {'results': results, 'query': query})

    elif request.GET.get('url'):
        url = request.GET.get('url')
        print(url)
        click = Click.objects.filter(url=url).order_by('-id').first()
        if click:
            print()
            click.click_count += 1
            click.save()
        else:
            click = Click.objects.create(url=url, click_count=1)
        return redirect("https://" + url)

    else:
        return render(request, 'search.html')
