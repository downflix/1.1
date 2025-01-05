from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
# Create your views here.
def index(request):
    return render(request, "index.html")

def terms(request):
    return render(request,"terms.html")

def copy(request):
    return render(request, "copy.html")

def privacy(request):
    return render(request,"privacy.html")

@csrf_exempt
def fetch_videos(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            url = data.get('url')

            if not url:
                return JsonResponse({'error': 'No URL provided'}, status=400)

            options = webdriver.ChromeOptions()
            options.binary_location = "C://Program Files//BraveSoftware//Brave-Browser//Application//brave.exe"
            driver = webdriver.Chrome(options=options)

            # URL of the website with videos
            driver.get(url)

            # Wait for video elements to load
            driver.implicitly_wait(10)

            # Find all <video> elements
            video_elements = driver.find_elements(By.TAG_NAME, "video")

            # List to store video URLs
            video_urls = []

            for i, video in enumerate(video_elements):
                # Get the 'src' attribute of the <video> tag
                video_url = video.get_attribute("src")

                # If the <video> tag has no 'src', check for <source> tags
                if not video_url:
                    sources = video.find_elements(By.TAG_NAME, "source")
                    for source in sources:
                        video_url = source.get_attribute("src")
                        if video_url:
                            video_urls.append(video_url)

                # Add the video URL to the list if found
                if video_url:
                    video_urls.append(video_url)

            # Print the list of video URLs
            print("Found video URLs:")
            for url in video_urls:
                print(url)

            # Quit the driver
            driver.quit()

            # Return the list of videos as JSON response
            return JsonResponse({'videos': video_urls })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Only POST is allowed.'}, status=405)