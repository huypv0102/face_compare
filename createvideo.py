import ffmpeg
import json

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def line_appender(filename, line):
    with open(filename,"a") as f:
        f.write(line)

def thisWay():

    imageFile = "result.txt"
    welcome = "images/welcome.png"
    thankyou = "images/thanku.png"
    output = "video.mp4"
    # line_prepender(imageFile,"file '{image}'".format(image=welcome))
    # line_appender(imageFile,"file '{image}'\n".format(image=thankyou))
    ffmpeg.input(imageFile, r='1', f='concat', safe='0').output(output, vcodec='h264').overwrite_output().run()



def anotherWay():
    welcome = "images/welcome.png"
    thankyou = "images/thanku.png"
    jpeg_files = [welcome]
    with open("result.txt", "r") as f:
        imagePaths = f.readlines()
    for path in imagePaths:
        image = str.split(path)
        jpeg_files.append(image[1])
    jpeg_files.append(thankyou)
    print(jpeg_files)
    # Execute FFmpeg sub-process, with stdin pipe as input, and jpeg_pipe input format
    process = ffmpeg.input('pipe:', r='20', f='jpeg_pipe').output('video.mp4', vcodec='libx264').overwrite_output().run_async(pipe_stdin=True)

    # Iterate jpeg_files, read the content of each file and write it to stdin
    for in_file in jpeg_files:
        with open(in_file, 'rb') as f:
            # Read the JPEG file content to jpeg_data (bytes array)
            jpeg_data = f.read()

            # Write JPEG data to stdin pipe of FFmpeg process
            process.stdin.write(jpeg_data)

    # Close stdin pipe - FFmpeg fininsh encoding the output file.
    process.stdin.close()
    process.wait()


# anotherWay()
thisWay()