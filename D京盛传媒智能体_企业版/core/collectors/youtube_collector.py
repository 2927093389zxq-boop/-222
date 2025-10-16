import os
from googleapiclient.discovery import build

def fetch_channel_stats(channel_id: str):
    """
    Fetches statistics for a given YouTube channel ID.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return {"error": "YOUTUBE_API_KEY 未在 .env 文件中配置。"}

    try:
        # Build the service object
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Create the request
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        # Execute the request
        response = request.execute()

        if not response.get('items'):
            return {"error": "找不到频道，或API密钥无效。"}

        channel_data = response['items'][0]
        
        # Extract the relevant statistics
        stats = {
            "channel_name": channel_data['snippet']['title'],
            "description": channel_data['snippet']['description'][:200] + '...',
            "published_at": channel_data['snippet']['publishedAt'],
            "subscriber_count": int(channel_data['statistics'].get('subscriberCount', 0)),
            "video_count": int(channel_data['statistics']['videoCount']),
            "view_count": int(channel_data['statistics']['viewCount']),
        }
        return stats

    except Exception as e:
        return {"error": f"获取 YouTube 数据时出错: {e}"}
