import ffmpeg
import argparse
import os
import json
import shutil

def getImageListFrom(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data["data"]



def createVideo(imageFile, welcomeImage, thankUImage, output):
    imageList = getImageListFrom(imageFile)
    if len(imageList) % 2 != 0:
        imageList.append(imageList[len(imageList)-1])
    # Insert welcome and thank-you page
    imageList.append(thankUImage)
    imageList.insert(0, welcomeImage)

    outputList = []
    tempDir = "/tmp/videoFolder" + output + "/"
    os.mkdir(tempDir)
    # Create .mp4 file for each image 
    for i in range(len(imageList)):
        outname = tempDir + imageList[i].split("/")[-1] + '.mp4'
        os.system(
            f'ffmpeg -loop 1 -i {imageList[i]} -c:v libx264 -t 2 -pix_fmt yuv420p -vf scale=320:240 {outname} -y')
        outputList.append(outname)
    
    open('concat.txt', 'w').writelines(
        [('file %s\n' % input_path) for input_path in outputList])
    ffmpeg.input('concat.txt', format='concat', safe=0).output(
        output + ".mp4", c='copy').overwrite_output().run()
    os.remove("concat.txt")
    shutil.rmtree(tempDir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--Path", help="File contains images path", required=True)
    parser.add_argument("-w", "--Welcome",
                        help="First slide", required=True)
    parser.add_argument("-t", "--Trailing",
                        help="Last slide ", required=True)
    parser.add_argument("-o", "--Output",
                        help="Output file ", required=True)
    args = parser.parse_args()
    createVideo(imageFile=args.Path, welcomeImage=args.Welcome,
                thankUImage=args.Trailing, output=args.Output)
