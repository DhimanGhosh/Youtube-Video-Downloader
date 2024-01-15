import yt_dlp


def download_audio(url, output_path='./'):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        file_size = __get_video_size(ydl, url)
        if file_size:
            print(f'File size: {file_size} bytes')
        ydl.download([url])


def download_video(url, output_path='./'):
    options = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        file_size = __get_video_size(ydl, url)
        if file_size:
            print(f'File size: {file_size} bytes')
        ydl.download([url])


def __get_video_size(ydl, video_url):
    """
    get the video size in bytes

    :param ydl: YoutubeDL object
    :param video_url: YouTube video URL
    :return float: file_size (in bytes)
    """
    info_dict = ydl.extract_info(video_url, download=False)
    file_size = info_dict.get('filesize')
    if file_size is not None:
        return file_size
    else:
        return None
