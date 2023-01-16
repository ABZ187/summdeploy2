from youtube_transcript_api import YouTubeTranscriptApi


class YoutubeToText:
    def __get_video_id(self, link):
        return link.split("=")[1]

    def get_text(self, link):
        text = ""
        video_id = self.__get_video_id(link)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for i in transcript:
            text += ' ' + i['text']
        return text
