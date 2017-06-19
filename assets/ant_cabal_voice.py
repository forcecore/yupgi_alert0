import glob
import os
import sys

# http://sox.sourceforge.net/sox.html

def make_ch1(inf):
    ouf = fname.replace("ch0", "ch1")

    # -15%
    # Semitone... so you better use
    # -281 = -2.81 semitones. (computed by audacity)
    cmd = "sox {} {} pitch -281".format(inf, ouf)
    print(cmd)
    os.system(cmd)

def make_ch2(inf):
    ouf = fname.replace("ch0", "ch2")

    # -20%
    # Semitone... so you better use
    # -386 = -3.86 semitones. (computed by audacity)
    cmd = "sox {} {} " \
        + "pitch -386 " \
        + "echo 1 1 500 0.6 " \
        + "gain -5"
    cmd = cmd.format(inf, ouf)
    print(cmd)
    os.system(cmd)

    cmd = "sox {} {}.wav fade 0 0 1".format(ouf, ouf)
    print(cmd)
    os.system(cmd)
    print()

def make_ch3(inf):
    # Let's use already pitched one
    inf = inf.replace("ch0", "ch1")

    ouf = fname.replace("ch0", "ch3")

    #[reverberance (50%) [HF-damping (50%)
    #[room-scale (100%) [stereo-depth (100%) 
    #[pre-delay (0ms) [wet-gain (0dB)]]]]]]

    cmd = "sox {} {} " \
        + "reverse " \
        + "reverb 50 50 100 80 20 10 " \
        + "reverse " \
        + "gain -5"
    cmd = cmd.format(inf, ouf)
    print(cmd)
    os.system(cmd)

def merge(inf):
    ch1 = fname.replace("ch0", "ch1")
    ch2 = fname.replace("ch0", "ch2") + ".wav"
    ch3 = fname.replace("ch0", "ch3")
    out = fname.replace("ch0", "out")

    # -m decreases the volume so you need combine mix,
    # with -v 1 specification.
    cmd = "sox --combine mix "
    for xx in [ch1, ch2, ch3]:
        cmd += "-v 1 " + xx + " "
    cmd += out
    print(cmd)
    os.system(cmd)

for fname in glob.glob("ch0/*.wav"):
    make_ch1(fname)
    make_ch2(fname)
    make_ch3(fname)
    merge(fname)
