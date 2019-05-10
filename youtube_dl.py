#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 
usage:
    ydl.py [-h|--help] [-u|--url <youtube_url>] [-d|--directory <path>] [-l|--leave]
 
options:
    -h, --help                show this help message and exit
    -u, --url <youtube_url>   designate youtube url
    -d, --directory <path>    designate directory to save video
    -l, --leave               leave original file. (this program conbines video and audio file ) 
 
"""

# [notion]
# $ pip install pytube
# needed

from pytube import YouTube
import sys, os, subprocess
from docopt import docopt

# print( sys.getdefaultencoding() )

dl_dir = "./"
dl_link = "none"

total_bytes = -1
def show_progress_bar(stream, chunk, file_handle, bytes_remaining ):
    global total_bytes
    if total_bytes == -1:
        total_bytes = bytes_remaining

    # progress_str = str( total_bytes - bytes_remaining ) + " / " + total_bytes + " bytes downloaded."
    print( (total_bytes-bytes_remaining), "/", total_bytes, "bytes downloaded.", end='\r', flush=True)

    # sys.stdout.write("\r\033[K")
    # sys.stdout.flush()
    return

# if not os.path.exists( dl_dir_video ):
#     os.makedirs( dl_dir_video )
# if not os.path.exists( dl_dir_audio ):
#     os.makedirs( dl_dir_audio )
# if not os.path.exists( dl_dir_both ):
#     os.makedirs( dl_dir_both )
args = docopt(__doc__)
print( args )
if len( args['--url'] ) == 0:
    print( "Download link" )
    dl_link = input( " >>> " )
else:
    dl_link = args['--url'][0]

if dl_link.find('https') != 0:
    dl_link = 'https://www.youtube.com/watch?v=' + dl_link

if len( args['--directory'] ) != 0:
    dl_dir = args['--directory'][0]
    print( dl_dir )

if not os.path.exists( dl_dir ):
    os.makedirs( dl_dir )

    

yt = YouTube( dl_link )
yt.register_on_progress_callback( show_progress_bar )

# targets = yt.streams.all()
# for el in targets:
#     print( el )
# sys.exit()

# print( "Whitch to DL?" )
# itag = input( ">>>" )
#
# print( "Start downloading." )
# yt.streams.get_by_itag( itag ).download( dl_dir_video )
# print( "\nFinish downloading." )
# sys.exit()

# print( "### all" )
# for el in yt.streams.filter( progressive=False ).all():
#     print( el )
# print( "### video" )
# for el in yt.streams.filter( progressive=False, mime_type="video/mp4" ).all():
#     print( el )
# print( "### audio" )
# for el in yt.streams.filter( progressive=False, mime_type="audio/mp4" ).all():
#     print( el )

target_res_list = [ "1080p", "720p", "480p", "360p" ]

for target_res in target_res_list:
    target_video = yt.streams.filter( res=target_res ).first()
    if target_video is not None:
        break

if target_video is None:
    print( "cannot find target resolution" )
    sys.exit()

# target_video = yt.streams.filter( mime_type="video/mp4").order_by('resolution').desc().first()
target_audio = yt.streams.filter( mime_type="audio/mp4" ).order_by('abr').desc().first()
print( target_video )

# somewhat '.' is replaced with space
escape_chars = [ '.', '/' ]
title = yt.title
for ec in escape_chars:
    title = title.replace( ec, '' )


audio_path = dl_dir + "/" + title + "_audio.mp4" 
video_path = dl_dir + "/" + title + "_video.mp4" 
output_path = dl_dir + "/" + title + ".mp4" 

print( title )
print( "Start downloading video." )
target_video.download( dl_dir, title + "_video" )
print( "\nFinish downloading." )
print( target_audio )
print( "Start downloading audio." )
target_audio.download( dl_dir, title + "_audio" )
print( "\nFinish downloading." )

# convert audio and video
cmd = "ffmpeg"
cmd += " -i \"" + video_path + "\""
cmd += " -i \"" + audio_path + "\""
cmd += " -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 " + "\"" + output_path + "\""
print( "ffmpeg cmd : ", cmd )
subprocess.call( cmd, shell=True ) 

if not args['--leave']:
    os.remove( audio_path )
    os.remove( video_path )
