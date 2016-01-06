# https://www.youtube.com/watch?v=7qn7VnXZb8I

import pychromecast

def play():
    cast = pychromecast.get_chromecast()
    mc = cast.media_controller
    cast.wait()
    mc.play_media(
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/" +
        "sample/BigBuckBunny.mp4", "video/mp4")

def pause():
    cast = pychromecast.get_chromecast()
    mc = cast.media_controller
    cast.wait()
    mc.stop()
