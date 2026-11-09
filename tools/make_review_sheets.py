"""Make review material from a finished MP4 (for the QA subagents).
usage: python tools/make_review_sheets.py <video.mp4> <out_dir> [step_seconds=2.5]
Writes: out_dir/sheet_XX.png (6 frames per sheet, in time order; sheet_XX_times.txt lists the times), out_dir/ffprobe.txt, out_dir/diffs.txt (adjacent-frame spikes).
Needs ffmpeg/ffprobe in PATH; numpy only for diffs (optional)."""
import subprocess, sys, os, json
video, out = sys.argv[1], sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
os.makedirs(out, exist_ok=True)
probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames,duration,sample_rate,channels', '-of', 'default=nw=1', video], capture_output=True, text=True).stdout
open(os.path.join(out, 'ffprobe.txt'), 'w').write(probe)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout.strip())
times = []; t = 0.3
while t < dur - 0.2: times.append(round(t, 2)); t += step
for i in range(0, len(times), 6):
    grp = times[i:i + 6]; args = ['ffmpeg', '-v', 'error', '-y']; fc = ''
    for j, tt in enumerate(grp):
        args += ['-ss', str(tt), '-i', video]; fc += f"[{j}:v]scale=360:640[v{j}];"
    fc += ''.join(f'[v{j}]' for j in range(len(grp))) + f'hstack=inputs={len(grp)}'
    subprocess.run(args + ['-frames:v', '1', '-filter_complex', fc, os.path.join(out, f'sheet_{i // 6:02d}.png')], check=False)
    open(os.path.join(out, f'sheet_{i // 6:02d}_times.txt'), 'w').write(', '.join(f'{x}s' for x in grp))
try:
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 192, 108).astype(np.float32); d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    fps = a.shape[0] / dur; sp = [round((i + 1) / fps, 2) for i in range(2, len(d) - 2) if d[i] > 4 and d[i] > 2.2 * max(d[i - 2], d[i - 1], d[i + 1], d[i + 2])]
    open(os.path.join(out, 'diffs.txt'), 'w').write(f'median {np.median(d):.2f} max {d.max():.2f}\nisolated spikes (s): {sp}\n(spikes at subtitle/transition changes are expected)\n')
except Exception as e:
    open(os.path.join(out, 'diffs.txt'), 'w').write('diff analysis skipped: ' + str(e))
print('done', out)
