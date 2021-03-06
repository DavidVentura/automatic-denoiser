# Audio denoiser

This script removes background noise from video files.

This is custom built specifically to denoise the [Category Theory for Programmers](https://www.youtube.com/watch?v=O2lZkr-aAqk&list=PLbgaMIhjbmEnaH_LTkxLI7FMa2HsnawM_&index=3) playlist.

Example input: <a href="https://raw.githubusercontent.com/DavidVentura/automatic-denoiser/master/examples/input.mp3" target="_blank">audio file</a>

Example output: <a href="https://raw.githubusercontent.com/DavidVentura/automatic-denoiser/master/examples/output.mp3" target="_blank">audio file</a>

Example noise: <a href="https://raw.githubusercontent.com/DavidVentura/automatic-denoiser/master/examples/noise.mp3" target="_blank">audio file</a>


# Usage

```
$ python3 denoiser.py <video file>
# outputs `denoised-<file>`
```

# Requirements

* ffmpeg
* sox
* python-sox

# How it works

Reads an input file, extracts the audio as wav with ffmpeg and grabs as 'noise' the first non-zero audio that is not
"too" loud.  
The noise is then passed to nox to generate a profile, and later user that profile to remove the noise from the original
audio.  
The clean audio is then put back together with the video, on a newly-created file, named `denoised-<original filename>`


On noise-reduction:

from `man sox`:

```
noisered [profile-file [amount]]
    Reduce noise in the audio signal by profiling and filtering. This effect is moderately effective at removing consistent background noise such as hiss or hum.
```


