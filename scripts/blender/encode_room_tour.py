import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--frames', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--count', type=int, default=600)
parser.add_argument('--ffmpeg', default='ffmpeg')
args = parser.parse_args()
files = [args.frames.resolve() / f'{i:04}.jpg' for i in range(1, args.count + 1)]
assert all(p.is_file() for p in files), 'The frame sequence is incomplete'

# The rendered JPEGs use sRGB. Explicit tags prevent a brightness shift in playback.
colour = (
    'scale=in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,'
    'format=yuv420p,'
    'setparams=range=limited:color_primaries=bt709:color_trc=iec61966-2-1:colorspace=bt709'
)
subprocess.run([
    args.ffmpeg, '-y', '-hide_banner', '-loglevel', 'warning',
    '-framerate', '30', '-i', str(args.frames.resolve() / '%04d.jpg'),
    '-frames:v', str(args.count), '-vf', colour,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-color_primaries', 'bt709', '-colorspace', 'bt709',
    '-color_trc', 'iec61966-2-1', '-movflags', '+faststart', '-an',
    str(args.output.resolve()),
], check=True)
print('TOUR_ENCODE_COMPLETE', args.output.resolve(), flush=True)
