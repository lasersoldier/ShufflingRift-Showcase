#!/usr/bin/env python3
"""Cut a promo trailer from a raw gameplay recording with ffmpeg.

Usage:
  python tools/make_trailer.py "D:/video/ShufflingRift Demo.mkv" out/trailer.mp4 \
      [--ffmpeg D:/oopz/ffmpeg.exe] [--music track.mp3] [--vertical]

Edit SEGMENTS below (start/end in seconds of the source, bilingual caption) and re-run.
No music is bundled: pass --music only with a track you have the rights to use.
"""
import argparse, os, subprocess, sys, tempfile

FONT = r"C\:/Windows/Fonts/msyh.ttc"   # Microsoft YaHei, covers CJK + Latin
W, H, FPS = 1920, 1080, 60
FADE = 0.35

# (start, end, zh, en)
SEGMENTS = [
    (0,   4,   "一家卡牌店，和一条街",            "A card shop, and the street around it"),
    (6,   10,  "九种人格，各有天赋与代价",        "Nine personas, each with talents and trade-offs"),
    (18,  23,  "上网批发进货",                    "Order stock from the in-game computer"),
    (42,  50,  "每张卡都是真实存在的唯一实体",    "Every card is a unique physical object"),
    (59,  69,  "店内自带卡牌对战《碎裂时空》",    "A full TCG built right into the shop"),
    (86,  100, "在实体牌桌上对战",              "Play on real, physical tables"),
    (114, 123, "街对面：当铺、渔具店……",          "Across the street: pawn shop, tackle shop and more"),
    (128, 138, "顾客、卖家与对战客",              "Customers, sellers and duelists"),
    (164, 176, "后院河边钓鱼",                    "Fish by the river out back"),
    (180, 190, "对抗张力，别让线断",              "Fight the line tension"),
    (216, 230, "五格渔具，自由搭配",              "Five-slot tackle loadouts"),
    (240, 248, "卡册与组牌",                      "Binder and deck building"),
    (250, 258, "一家热闹的店",                    "A shop that feels alive"),
]
TITLE = ("碎裂时空", "SHUFFLING RIFT", "一家卡牌店，和一条街")
END = ("碎裂时空", "github.com/lasersoldier/ShufflingRift-Showcase")


def esc_file(path):
    return path.replace("\\", "/").replace(":", chr(92) + ":")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--music")
    ap.add_argument("--vertical", action="store_true", help="also write a 9:16 center-crop")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="trailer_")

    def tf(name, text):
        p = os.path.join(tmp, name)
        open(p, "w", encoding="utf-8").write(text)
        return esc_file(p)

    cmd = [a.ffmpeg, "-hide_banner", "-y"]
    for s, e, *_ in SEGMENTS:
        cmd += ["-ss", str(s), "-t", str(e - s), "-i", a.src]
    n = len(SEGMENTS)
    if a.music:
        cmd += ["-i", a.music]
    f, labels = [], []
    # title card
    t_zh, t_en, t_sub = TITLE
    f.append(
        f"color=c=0x0d1117:s={W}x{H}:r={FPS}:d=3,"
        f"drawtext=fontfile='{FONT}':textfile='{tf('t1.txt', t_zh)}':fontsize=140:fontcolor=white:x=(w-tw)/2:y=h/2-150,"
        f"drawtext=fontfile='{FONT}':textfile='{tf('t2.txt', t_en)}':fontsize=54:fontcolor=0xe3b341:x=(w-tw)/2:y=h/2+10,"
        f"drawtext=fontfile='{FONT}':textfile='{tf('t3.txt', t_sub)}':fontsize=40:fontcolor=0xaaaaaa:x=(w-tw)/2:y=h/2+110,"
        f"fade=t=in:d=0.6,fade=t=out:st=2.4:d=0.6,format=yuv420p[title]")
    labels.append("[title]")
    for i, (s, e, zh, en) in enumerate(SEGMENTS):
        d = e - s
        alpha = rf"if(lt(t\,{FADE})\,t/{FADE}\,if(gt(t\,{d - FADE})\,({d}-t)/{FADE}\,1))"
        f.append(
            f"[{i}:v]setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,"
            f"drawtext=fontfile='{FONT}':textfile='{tf(f'z{i}.txt', zh)}':fontsize=54:fontcolor=white:alpha='{alpha}':"
            f"x=70:y=h-190:box=1:boxcolor=black@0.45:boxborderw=18,"
            f"drawtext=fontfile='{FONT}':textfile='{tf(f'e{i}.txt', en)}':fontsize=34:fontcolor=0xe3b341:alpha='{alpha}':"
            f"x=70:y=h-110:box=1:boxcolor=black@0.45:boxborderw=12,"
            f"fade=t=in:d={FADE},fade=t=out:st={d - FADE}:d={FADE},format=yuv420p[v{i}]")
        labels.append(f"[v{i}]")
    e_zh, e_url = END
    f.append(
        f"color=c=0x0d1117:s={W}x{H}:r={FPS}:d=4,"
        f"drawtext=fontfile='{FONT}':textfile='{tf('n1.txt', e_zh)}':fontsize=120:fontcolor=white:x=(w-tw)/2:y=h/2-110,"
        f"drawtext=fontfile='{FONT}':textfile='{tf('n2.txt', e_url)}':fontsize=40:fontcolor=0xe3b341:x=(w-tw)/2:y=h/2+50,"
        f"fade=t=in:d=0.6,fade=t=out:st=3.4:d=0.6,format=yuv420p[end]")
    labels.append("[end]")
    f.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[outv]")
    script = os.path.join(tmp, "filter.txt")
    open(script, "w", encoding="utf-8").write(";\n".join(f))

    total = 3 + sum(e - s for s, e, *_ in SEGMENTS) + 4
    cmd += ["-filter_complex_script", script, "-map", "[outv]"]
    if a.music:
        cmd += ["-map", f"{n}:a", "-af",
                f"afade=t=in:d=1.5,afade=t=out:st={total - 3}:d=3", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", a.out]
    print("running ffmpeg, total ~%ds" % total, flush=True)
    subprocess.run(cmd, check=True)

    if a.vertical:
        v = os.path.splitext(a.out)[0] + "_9x16.mp4"
        subprocess.run([a.ffmpeg, "-hide_banner", "-y", "-i", a.out, "-vf",
                        "crop=608:1080:656:0,scale=1080:1920", "-c:v", "libx264", "-crf", "20",
                        "-c:a", "copy", v], check=True)
        print("vertical:", v)
    print("done:", a.out)

if __name__ == "__main__":
    sys.exit(main())
