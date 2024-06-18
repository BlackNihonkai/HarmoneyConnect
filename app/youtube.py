import apiclient
import datetime
import isodate
import cnum


def change_time_format(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h == 0:
        if s < 10:
            return f'{m}:0{s}'
        else:
            return f'{m}:{s}'
    else:
        if m < 10 and s <10:
            return f'{h}:0{m}:0{s}'
        elif m < 10:
            return f'{h}:0{m}:{s}'
        elif s < 10:
            return f'{h}:{m}:0{s}'
        else:
            return f'{h}:{m}:{s}'


def get_search(youtube_api_key, keyword):
    youtube = apiclient.discovery.build('youtube', 'v3', developerKey = youtube_api_key)
    request = youtube.search().list(part = 'id, snippet', q = keyword, maxResults = 10, order = 'viewCount', type = 'video',)
    responses = request.execute()
    
    videos_parameters_list = []
    for response in responses['items']:
        video_obj = youtube.videos().list(part = 'statistics, contentDetails', id = response['id']['videoId']).execute()
        viewcount = video_obj['items'][0]['statistics']['viewCount']
        viewcount = cnum.jp(viewcount)

        video_time = video_obj['items'][0]['contentDetails']['duration']
        video_time = isodate.parse_duration(video_time).seconds
        video_time = change_time_format(video_time)

        channel_obj = youtube.channels().list(part = 'snippet', id = response['snippet']['channelId']).execute()
        profile_image_url = channel_obj['items'][0]['snippet']['thumbnails']['default']['url']
        channel_handle_id = channel_obj['items'][0]['snippet']['customUrl']

        published_at = datetime.datetime.strptime(response['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date()
        published_at = published_at.strftime(('%Y/%m/%d'))

        video_parameters_dict = {
            'viewcount' : viewcount,
            'profile_image_url' : profile_image_url,
            'video_time' : video_time,
            'published_at' : published_at,
            'title' : response['snippet']['title'],
            'channel_handle_id' : channel_handle_id,
            'channel_title' : response['snippet']['channelTitle'],
            'thumbnali_url' : response['snippet']['thumbnails']['medium']['url'],
            'description' : response['snippet']['description'],
            'video_id' : response['id']['videoId'],
        }

        videos_parameters_list.append(video_parameters_dict)
    return videos_parameters_list