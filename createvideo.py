import ffmpeg
import argparse
import os
import json
import shutil


def getImageListFrom(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data["data"]


def jpgToMp4(inputFilename, outputFilename, lineOneText, duration=7, clear=2, background='black'):
    SCALE_OPTIONS = {
        'force_original_aspect_ratio': 'decrease',
    }
    PAD_OPTIONS = {
        'width': 1920,
        'height': 1080,
        'x': '(ow-iw)/2',
        'y': '(oh-ih)/2',
        'color': background,
    }
    FADE_IN_OPTIONS = {
        'type': 'in',
        'start_time': '0',
        'duration': '1',
    }
    FADE_OUT_OPTIONS = {
        'type': 'out',
        'start_time': '%s' % (duration-1),
        'duration': '1',
    }

    LINE_ONE_TEXT_OPTIONS = {
        'text': lineOneText,
        'x': '((w-text_w)/2)',
        'y': '(h-text_h-30)',
        'fontfile': 'LiberationSans-Regular.ttf',
        'fontsize': '40',
        'fontcolor': 'white',
        'borderw': '4',
        'bordercolor': 'black',
        'alpha': 'if(lt(t,0),0,if(lt(t,1),(t-0)/1,if(lt(t,%d),1,if(lt(t,%d),(1-(t-%d))/1,0))))' % (duration-clear-1, duration-clear, duration-clear-1),
    }

    stream = ffmpeg.input(inputFilename, t=str(duration), loop=1)
    stream = stream.filter('scale', 1920, 1080, **SCALE_OPTIONS)
    stream = stream.filter('pad', 1920, 1080, **PAD_OPTIONS)
    stream = stream.filter('fade', **FADE_IN_OPTIONS)
    stream = stream.filter('fade', **FADE_OUT_OPTIONS)
    stream = stream.filter('drawtext', **LINE_ONE_TEXT_OPTIONS)
    stream.output(outputFilename, pix_fmt='yuv420p').run(overwrite_output=True)


def createSubVideo(imageList, dir, studentName):
    outputList = []
    for i in range(len(imageList)):
        outname = dir + imageList[i].split("/")[-1] + '.mp4'
        jpgToMp4(
            inputFilename=imageList[i], outputFilename=outname, lineOneText=studentName, duration=5)
        outputList.append(outname)

    return outputList


def mergeAudioAndVideo(audioFile, videoFile):
    cmd = f'ffprobe -v quiet -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {videoFile}.mp4'
    video_duration = os.popen(cmd).read()
    video_duration = float(str.strip(video_duration))

    ffmpeg.concat(ffmpeg.input(videoFile+".mp4"), ffmpeg.input(audioFile, t=video_duration),
                  v=1, a=1).output(videoFile + '.final.mp4').run(overwrite_output=True)


def createVideo(imageFile, welcomeImage, thankUImage, audioFile, output, studentName):
    imageList = getImageListFrom(imageFile)
    if len(imageList) % 2 != 0:
        imageList.append(imageList[len(imageList)-1])
    # Insert welcome and thank-you page
    imageList.append(thankUImage)
    imageList.insert(0, welcomeImage)

    outputList = []
    tempDir = "/tmp/videoFolder" + output + "/"
    os.mkdir(tempDir)
    outputList = createSubVideo(
        imageList=imageList, dir=tempDir, studentName=studentName)

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
        "-f", "--File", help="File contains images path", required=True)
    parser.add_argument("-w", "--Welcome",
                        help="First slide", required=True)
    parser.add_argument("-t", "--Trailing",
                        help="Last slide ", required=True)
    parser.add_argument("-a", "--Audio",
                        help="Audio file", required=True)
    parser.add_argument("-n", "--Name",
                        help="Student name", default="")

    parser.add_argument("-o", "--Output",
                        help="Output file (without .ext) ", required=True)
    args = parser.parse_args()
    createVideo(imageFile=args.File, welcomeImage=args.Welcome,
                thankUImage=args.Trailing, output=args.Output, audioFile=args.Audio, studentName=args.Name)
