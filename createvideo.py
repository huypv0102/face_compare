import ffmpeg
import argparse
import os
import json
import shutil
import tqdm


def getImageListFrom(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data["data"]


def jpgToMp4(inputFilename, outputFilename,  duration=7, background='black'):
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

    stream = ffmpeg.input(inputFilename, t=str(duration), loop=1)
    stream = stream.filter('scale', 1920, 1080, **SCALE_OPTIONS)
    stream = stream.filter('pad', 1920, 1080, **PAD_OPTIONS)
    stream = stream.filter('fade', **FADE_IN_OPTIONS)
    stream = stream.filter('fade', **FADE_OUT_OPTIONS)
    stream.output(outputFilename, pix_fmt='yuv420p').run(overwrite_output=True, quiet = True)


def createSubVideo(imageList, dir, duration):
    outputList = []
    bar = tqdm.tqdm(total=len(
        imageList), desc="Creating sub videos" , position=1)
    for i in range(len(imageList)):
        bar.update(1)
        outputPath = dir + imageList[i].split("/")[-1] + '.mp4'
        jpgToMp4(
            inputFilename=imageList[i], outputFilename=outputPath, duration=duration)

        outputList.append(outputPath)

    return outputList


def mergeAudioAndVideo(audioFile, videoFile):
    bar = tqdm.tqdm(total=1, desc="Merging audio and video" , position=1)
    metadata = ffmpeg.probe(videoFile+".mp4")
    video_duration = float(metadata['format']['duration'])
    ffmpeg.concat(ffmpeg.input(videoFile+".mp4"), ffmpeg.input(audioFile, t=video_duration),
                  v=1, a=1).output(videoFile + '.final.mp4').run(overwrite_output=True, quiet = True)
    bar.update(1)


def createVideo(imageFile,  thankUImage, audioFile, output, studentName, duration):
    imageList = getImageListFrom(imageFile)
    imageList.append(thankUImage)

    outputList = []
    tempDir = "tmpVideos/"
    if not os.path.exists(tempDir):
        os.makedirs(tempDir)

    outputList = createSubVideo(
        imageList=imageList, dir=tempDir, duration=duration)

    open('concat.txt', 'w').writelines(
        [('file %s\n' % input_path) for input_path in outputList])

    TEXT_OPTIONS = {
        'text': studentName,
        'x': '((w-text_w)/2)',
        'y': '((h-text_h)/3)',
        'fontfile': 'LiberationSans-Regular.ttf',
        'fontsize': '80',
        'fontcolor': 'white',
        'borderw': '4',
        'bordercolor': 'black',
        'alpha': 'if(lt(t,0),0,if(lt(t,1),(t-0)/1,if(lt(t,%d),1,if(lt(t,%d),(1-(t-%d))/1,0))))' % (duration, duration, duration),
    }
    ffmpeg.input('concat.txt', format='concat', safe=0).filter('drawtext', **TEXT_OPTIONS).output(
        output + ".mp4").overwrite_output().run(quiet = True)

    mergeAudioAndVideo(audioFile=audioFile, videoFile=output)


    os.remove(output + ".mp4")
    os.remove("concat.txt")
    shutil.rmtree(tempDir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-f", "--File", help="File contains images path", required=True)
    parser.add_argument("-t", "--Trailing",
                        help="Last slide ", required=True)
    parser.add_argument("-a", "--Audio",
                        help="Audio file", required=True)
    parser.add_argument("-n", "--Name",
                        help="Student name",required=True)

    parser.add_argument("-o", "--Output",
                        help="Output file (without .ext) ", required=True)
    parser.add_argument("-d", "--Duration",
                        help="Duration for each image ", default=4, type=int)

    args = parser.parse_args()
    createVideo(imageFile=args.File, thankUImage=args.Trailing,
                output=args.Output, audioFile=args.Audio, studentName=args.Name, duration=args.Duration)
