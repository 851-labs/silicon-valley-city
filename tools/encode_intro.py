"""Validate and encode the rendered intro; optionally add local reference audio."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FPS = '24000/1001'
FRAME_COUNT = 261


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference-audio', action='store_true',
                        help='Also write an ignored local mix with reference music')
    args = parser.parse_args()
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:
        parser.error('FFmpeg and ffprobe must be installed and available on PATH')

    folder = ROOT / 'animation'
    frames = folder / 'frames'
    spec = json.loads((frames / 'render_manifest.json').read_text())
    expected = list(range(1, FRAME_COUNT + 1))
    if spec['frames'] != expected:
        raise ValueError('A complete 261-frame render is required')
    if spec['scene_sha256'] != digest(folder / 'intro.blend'):
        raise ValueError('The saved Blender scene changed after rendering began')
    for number in expected:
        path = frames / f'frame_{number:04d}.png'
        with path.open('rb') as stream:
            header = stream.read(24)
        if header[:16] != b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR':
            raise ValueError(f'Invalid PNG header: {path}')
        if struct.unpack('>II', header[16:24]) != (spec['width'], spec['height']):
            raise ValueError(f'Unexpected frame dimensions: {path}')

    output = folder / 'intro.mp4'
    temporary = folder / 'intro.part.mp4'
    subprocess.run([
        ffmpeg, '-hide_banner', '-loglevel', 'warning', '-xerror', '-y',
        '-framerate', FPS, '-start_number', '1',
        '-i', str(frames / 'frame_%04d.png'), '-frames:v', str(FRAME_COUNT),
        '-vf', 'scale=in_range=full:out_range=tv:out_color_matrix=bt709',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
        '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-colorspace', 'bt709',
        '-color_primaries', 'bt709', '-color_trc', 'bt709',
        '-movflags', '+faststart', '-an', str(temporary),
    ], check=True)
    probe = json.loads(subprocess.check_output([
        ffprobe, '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_streams', '-of', 'json', str(temporary),
    ]))['streams'][0]
    if (probe['codec_name'] != 'h264' or probe['pix_fmt'] != 'yuv420p'
            or probe['avg_frame_rate'] != FPS
            or probe.get('color_space') != 'bt709'
            or int(probe['nb_read_frames']) != FRAME_COUNT
            or (probe['width'], probe['height']) != (spec['width'], spec['height'])):
        raise ValueError(f'Encoded video failed validation: {probe}')
    subprocess.run([
        ffmpeg, '-v', 'error', '-xerror', '-i', str(temporary), '-f', 'null', '-',
    ], check=True)
    temporary.replace(output)
    shutil.copy2(frames / 'frame_0192.png', folder / 'poster.png')
    report = {
        'result': 'PASS', 'frames': FRAME_COUNT, 'fps': FPS,
        'duration_seconds': float(probe['duration']),
        'resolution': [probe['width'], probe['height']],
        'codec': probe['codec_name'], 'pixel_format': probe['pix_fmt'],
        'color_space': probe['color_space'], 'color_range': probe['color_range'],
        'audio': False, 'scene_sha256': spec['scene_sha256'],
        'video_sha256': digest(output), 'bytes': output.stat().st_size,
        'render_samples': spec['samples'], 'render_device': spec['device'],
        'checks': ['complete PNG sequence', 'matching scene hash',
                   'frame dimensions', 'decoded frame count', 'full MP4 decode'],
    }
    (folder / 'video_validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('INTRO_VIDEO_VALIDATED', json.dumps(report), flush=True)

    if args.reference_audio:
        reference = ROOT / 'references/season1_intro.mp4'
        if not reference.is_file():
            raise FileNotFoundError(reference)
        local = folder / 'intro_with_reference_audio.mp4'
        subprocess.run([
            ffmpeg, '-hide_banner', '-loglevel', 'warning', '-y',
            '-i', str(output), '-i', str(reference), '-map', '0:v:0', '-map', '1:a:0',
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
            '-movflags', '+faststart', str(local),
        ], check=True)
        print('ENCODED_LOCAL_REFERENCE_AUDIO', local, flush=True)


if __name__ == '__main__':
    main()
