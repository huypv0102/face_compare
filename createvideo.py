import ffmpeg
import argparse
import os
import json
import shutil
import subprocess


def getImageListFrom(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data["data"]


def createSubVideo(imageList, dir):
    outputList = []
    for i in range(len(imageList)):
        outname = dir + imageList[i].split("/")[-1] + '.mp4'
        os.system(
            f'ffmpeg -loop 1 -i {imageList[i]} -c:v libx264 -t 2 -pix_fmt yuv420p -vf scale=1920:1080 {outname} -y')
        outputList.append(outname)

    return outputList


def mergeAudioAndVideo(audioFile, videoFile):
    cmd = f'ffprobe -v quiet -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {videoFile}.mp4'
    video_duration = os.popen(cmd).read()
    video_duration = float(str.strip(video_duration))

    ffmpeg.concat(ffmpeg.input(videoFile+".mp4"), ffmpeg.input(audioFile, t=video_duration),
                  v=1, a=1).output(videoFile + '.final.mp4').run(overwrite_output=True)


def createVideo(imageFile, welcomeImage, thankUImage, audioFile, output):
    imageList = getImageListFrom(imageFile)
    if len(imageList) % 2 != 0:
        imageList.append(imageList[len(imageList)-1])
    # Insert welcome and thank-you page
    imageList.append(thankUImage)
    imageList.insert(0, welcomeImage)

    outputList = []
    tempDir = "/tmp/videoFolder" + output + "/"
    os.mkdir(tempDir)
    outputList = createSubVideo(imageList=imageList, dir=tempDir)

    open('concat.txt', 'w').writelines(
        [('file %s\n' % input_path) for input_path in outputList])

    ffmpeg.input('concat.txt', format='concat', safe=0).output(
        output + ".mp4", c='copy').overwrite_output().run()

    os.remove("concat.txt")
    shutil.rmtree(tempDir)

    mergeAudioAndVideo(audioFile=audioFile, videoFile=output)
    os.remove(output + ".mp4")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--Path", help="File contains images path", required=True)
    parser.add_argument("-w", "--Welcome",
                        help="First slide", required=True)
    parser.add_argument("-t", "--Trailing",
                        help="Last slide ", required=True)
    parser.add_argument("-a", "--Audio",
                        help="Audio file", required=True)
    
    parser.add_argument("-o", "--Output",
                        help="Output file (without .ext) ", required=True)
    args = parser.parse_args()
    createVideo(imageFile=args.Path, welcomeImage=args.Welcome,
                thankUImage=args.Trailing, output=args.Output, audioFile=args.Audio)
