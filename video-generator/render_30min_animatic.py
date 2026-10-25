#!/usr/bin/env python3
"""Build a free 30-minute illustrated animatic with Pillow and FFmpeg."""
import math, os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 360, 640
FPS = 8
SCENE_SECONDS = 180
OUT = "the-girl-who-heard-her-dead-mother-30min-animatic.mp4"
SCENES = [
 ("THE HOUSE THAT LISTENS", "Rain falls over Amara's family home. A whisper calls her name.", "house"),
 ("MORNING DOES NOT EXPLAIN", "Uncle Emeka denies hearing anything, but his fear gives him away.", "kitchen"),
 ("THE MESSAGE", "A message arrives from her mother's disconnected phone number.", "phone"),
 ("THE LOCKED DOOR", "Amara finds a key and opens the sewing room that has been locked for years.", "door"),
 ("THE VOICE ON THE TAPE", "A cassette reveals a family secret and a story that may not be complete.", "tape"),
 ("THE GARDEN", "Amara and Nneka search beneath the old tree for a hidden letter.", "garden"),
 ("WHAT THE RECORDING CANNOT PROVE", "A final recording complicates everything Amara thought she knew.", "memory"),
 ("THE CONFESSION", "Emeka admits his lie. Amara refuses to confuse remorse with forgiveness.", "confession"),
 ("GOODBYE, MAMA", "In the sewing room, Amara listens to her mother's last words.", "sunrise"),
 ("THE LAST WHISPER", "At dawn, a final whisper leaves Amara with a choice to keep living.", "dawn"),
]

def getfont(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)

def wrap(draw, text, font, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=font)[2] <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def make_card(index, title, description, motif):
    im = Image.new("RGB", (W,H))
    p = im.load()
    for y in range(H):
        for x in range(W):
            glow = max(0, 1 - math.sqrt(((x-W*.52)/(W*.9))**2 + ((y-H*.3)/(H*.8))**2))
            p[x,y] = (int(3+glow*8), int(6+glow*15), int(14+glow*28))
    d = ImageDraw.Draw(im, "RGBA")
    # Moon, rain and distant trees.
    d.ellipse((255,62,318,125), fill=(175,197,222,180))
    d.ellipse((273,50,329,105), fill=(5,8,19,255))
    for i in range(12):
        x = (i*37 + index*13) % W
        d.line((x, 125+(i*19)%300, x-14, 190+(i*19)%300), fill=(115,150,185,55), width=2)
    for x in range(-10,W+30,34):
        h = 70 + ((x*7+index*17) % 80)
        d.polygon([(x-24,430),(x,430-h),(x+23,430)], fill=(5,10,18,255))
    if motif in ("house","dawn","sunrise"):
        d.polygon([(38,400),(180,295),(322,400)], fill=(10,14,25,255))
        d.rectangle((62,398,298,550), fill=(13,17,27,255), outline=(65,79,100,255), width=2)
        d.rectangle((91,430,139,490), fill=(224,177,108,95))
        d.rectangle((218,430,266,490), fill=(90,137,190,90))
        d.rectangle((160,470,201,550), fill=(2,4,10,255))
    elif motif in ("door","tape","memory","confession"):
        d.polygon([(36,150),(324,150),(286,520),(74,520)], fill=(10,13,24,255))
        d.rectangle((123,215,237,450), fill=(2,4,10,255), outline=(92,111,139,190), width=3)
        d.ellipse((220,320,229,329), fill=(218,182,121,220))
        if motif == "tape":
            d.rounded_rectangle((92,465,268,530), radius=8, fill=(25,28,38,255), outline=(145,158,176,200), width=2)
            d.ellipse((115,480,155,520), outline=(170,180,196,220), width=4)
            d.ellipse((205,480,245,520), outline=(170,180,196,220), width=4)
    elif motif in ("phone","kitchen"):
        d.rectangle((0,470,W,H), fill=(20,15,19,255))
        d.rounded_rectangle((130,310,230,485), radius=15, fill=(2,4,9,255), outline=(120,142,172,255), width=3)
        d.rectangle((140,330,220,455), fill=(18,32,54,255))
        d.ellipse((166,355,194,383), fill=(112,157,214,220))
        d.text((153,400),"MAMA",font=getfont(13,True),fill=(240,242,250,255))
    elif motif == "garden":
        d.rectangle((0,470,W,H), fill=(5,18,13,255))
        d.rectangle((165,235,195,490), fill=(36,26,19,255))
        d.ellipse((70,160,290,340), fill=(8,26,18,255), outline=(30,60,38,255), width=3)
        d.ellipse((164,460,198,480), fill=(175,151,111,255))
    else:
        d.ellipse((125,190,235,300), fill=(2,4,9,255))
        d.polygon([(105,290),(255,290),(286,520),(74,520)], fill=(3,5,11,255))
    # soft vignette
    shade = Image.new("L",(W,H),0)
    sd=ImageDraw.Draw(shade)
    sd.ellipse((-80,-80,W+80,H+80),fill=130)
    shade=shade.filter(ImageFilter.GaussianBlur(45))
    im=Image.composite(Image.new("RGB",(W,H),(0,0,0)),im,shade)
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle((0,0,W,86), fill=(0,0,0,180))
    d.text((18,20),"THE GIRL WHO HEARD HER DEAD MOTHER",font=getfont(11,True),fill=(182,200,224,255))
    d.text((18,55),f"CHAPTER {index+1:02d} / 10",font=getfont(12,True),fill=(223,181,130,255))
    d.rounded_rectangle((16,535,344,622), radius=12, fill=(0,0,0,190), outline=(103,125,154,120), width=1)
    d.text((27,548),title,font=getfont(14,True),fill=(244,241,233,255))
    lines=wrap(d,description,getfont(11),300)
    for j,line in enumerate(lines[:3]):
        d.text((27,572+j*15),line,font=getfont(11),fill=(190,204,223,255))
    return im

def run(cmd):
    subprocess.run(cmd, check=True)

def main():
    os.makedirs("animatic_scenes", exist_ok=True)
    with open("scene-list.txt","w",encoding="utf-8") as f:
        f.write("30-minute illustrated animatic - 10 chapters x 3 minutes\n\n")
        for i,(title,desc,motif) in enumerate(SCENES):
            f.write(f"{i+1:02d}. {title}\n{desc}\n\n")
    segment_files=[]
    for i,(title,desc,motif) in enumerate(SCENES):
        img=f"animatic_scenes/scene_{i+1:02d}.png"
        make_card(i,title,desc,motif).save(img)
        seg=f"animatic_scenes/segment_{i+1:02d}.mp4"
        # Slow, subtle zoom gives the still illustration a moving-camera feel.
        vf=f"zoompan=z='min(zoom+0.000035,1.035)':d=1:s={W}x{H}:fps={FPS},format=yuv420p"
        run(["ffmpeg","-y","-v","error","-loop","1","-i",img,"-t",str(SCENE_SECONDS),
             "-vf",vf,"-r",str(FPS),"-an","-c:v","libx264","-preset","ultrafast","-crf","29",seg])
        segment_files.append(seg)
        print(f"Rendered chapter {i+1}/10",flush=True)
    with open("animatic_scenes/concat.txt","w",encoding="utf-8") as f:
        for seg in segment_files:
            f.write("file '"+os.path.abspath(seg)+"'\n")
    run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i","animatic_scenes/concat.txt",
         "-f","lavfi","-i","sine=frequency=55:sample_rate=44100:duration=1800",
         "-f","lavfi","-i","sine=frequency=82.41:sample_rate=44100:duration=1800",
         "-filter_complex","[1:a]volume=0.10,afade=t=in:st=0:d=8,afade=t=out:st=1790:d=10[a0];[2:a]volume=0.035,afade=t=in:st=15:d=10,afade=t=out:st=1780:d=15[a1];[a0][a1]amix=inputs=2:normalize=0,alimiter=limit=0.85[a]",
         "-map","0:v:0","-map","[a]","-t","1800","-c:v","libx264","-preset","ultrafast","-crf","29",
         "-c:a","aac","-b:a","96k","-movflags","+faststart",OUT])
    duration=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",OUT],text=True).strip()
    print(f"Created {OUT}; duration={duration} seconds",flush=True)

if __name__ == "__main__":
    main()
