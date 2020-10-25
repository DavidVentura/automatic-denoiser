import math
import os
import shlex
import struct
import subprocess
import sys
import wave

import sox

CHUNK = 1024


SAMPLE_RATE = 44100

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

def rms(data):
    count = len(data)/2
    fmt = "%dh"%(count)
    shorts = struct.unpack( fmt, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt(sum_squares / count)



def find_noise(path):
    wf = wave.open(path, 'rb')
    data = wf.readframes(CHUNK)

    fc = 0
    noise_start = 0
    while data != '':
        r = rms(data)
        if r >= 0.000001 and noise_start == 0:
            noise_start = fc * CHUNK / SAMPLE_RATE

        if r >= 0.1:
            noise_end = fc * CHUNK / SAMPLE_RATE
            break

        fc += 1 
        data = wf.readframes(CHUNK)

    return noise_start, noise_end

def remove_noise(file_path):
    bname = os.path.basename(file_path)
    p = subprocess.Popen(['ffmpeg', '-i', file_path] + shlex.split(f'-c:a pcm_s16le -ar {SAMPLE_RATE} -y entire-audio.wav'),
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    p.wait()
    if p.returncode != 0:
        print('error!')
        exit(1)

    noise_start, noise_end = find_noise('entire-audio.wav')
    tfm = sox.Transformer()
    tfm.trim(noise_start, noise_end)
    tfm.build_file('entire-audio.wav', 'noise-sample.wav')

    tfm = sox.Transformer()
    tfm.noiseprof('noise-sample.wav', 'noise.prof')
    tfm.noisered('noise.prof', amount=0.21)
    tfm.build_file('entire-audio.wav', 'denoised.wav')

    cmd = ['ffmpeg', '-i', file_path] + shlex.split(f'-i denoised.wav -map 0:v -map 1:a -c:v copy') + [f'denoised-{bname}']

    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    p.wait()
    if p.returncode != 0:
        exit(1)

remove_noise(sys.argv[1])
