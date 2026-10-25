#!/usr/bin/env python3
"""Render a 15-second vertical cinematic mystery short using Pillow and FFmpeg."""
import math
import os
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DURATION = 450, 800, 15, 15
TOTAL = FPS * DURATION
OUT = "the-girl-who-heard-her-dead-mother.mp4"
random.seed(19)

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

TITLE = font(35, True)
SUB = font(18, True)
SMALL = font(15)
BIG = font(28, True)

def gradient(seed):
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            glow = max(0, 1 - math.sqrt(((x-W*.53)/(W*.8))**2 + ((y-H*.34)/(H*.7))**2))
            n = random.Random(seed + x//13 + y//17).randint(0, 4)
            px[x,y] = (int(3+glow*8+n), int(5+glow*13+n), int(13+glow*24+n))
    return im

def centered(draw, y, text, f, fill, spacing=5):
    box = draw.multiline_textbbox((0,0), text, font=f, spacing=spacing, align="center", stroke_width=0)
    draw.multiline_text(((W-(box[2]-box[0]))/2, y), text, font=f, fill=fill, spacing=spacing, align="center")

def draw_house(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    # moon and wisps
    d.ellipse((310,95,385,170), fill=(176,197,220,230))
    d.ellipse((330,82,395,145), fill=(5,8,19,255))
    for i in range(6):
        y = 270 + i*48 + int(math.sin(t*1.7+i)*12)
        d.arc((-100,y,540,y+90), 185, 350, fill=(110,139,169,20), width=3)
    # distant trees
    for x in range(-20, W+30, 48):
        h = 100 + (x*7 % 75)
        d.polygon([(x-30,510),(x,510-h),(x+28,510)], fill=(5,9,18,255))
    # house
    d.polygon([(75,460),(225,350),(375,460)], fill=(9,12,23,255))
    d.rectangle((100,455,350,665), fill=(12,15,25,255), outline=(53,65,83,255), width=3)
    d.rectangle((135,490,193,570), fill=(230,190,119,120))
    d.rectangle((258,490,316,570), fill=(220,190,140,70))
    d.line((164,490,164,570), fill=(16,19,30,255), width=4)
    d.line((135,530,193,530), fill=(16,19,30,255), width=4)
    d.rectangle((204,555,248,665), fill=(3,5,12,255))
    # foreground grass
    d.polygon([(0,700),(100,650),(180,710),(270,660),(450,700),(450,800),(0,800)], fill=(4,7,13,255))

def draw_girl(im, t):
    d = ImageDraw.Draw(im, "RGBA")
    # hallway vanishing point and floor
    d.polygon([(45,100),(405,100),(350,620),(100,620)], fill=(9,12,23,255))
    d.polygon([(45,100),(0,0),(0,800),(100,620)], fill=(5,7,15,255))
    d.polygon([(405,100),(450,0),(450,800),(350,620)], fill=(4,6,13,255))
    d.polygon([(100,620),(350,620),(450,800),(0,800)], fill=(13,17,29,255))
    for i in range(7):
        y=630+i*28
        d.line((max(0,180-i*23),y,min(W,270+i*23),y), fill=(75,88,110,22), width=2)
    # eerie door at end
    d.rectangle((165,170,285,420), fill=(2,4,10,255), outline=(89,101,122,150), width=3)
    d.ellipse((268,295,275,302), fill=(205,175,119,220))
    # girl silhouette in foreground
    x = 220 + int(math.sin(t*1.2)*5)
    d.ellipse((x-28,410,x+28,468), fill=(2,3,8,255))
    d.polygon([(x-24,455),(x+24,455),(x+52,650),(x-53,650)], fill=(3,4,10,255))
    d.polygon([(x-22,460),(x-48,555),(x-65,595),(x-50,600),(x-10,555)], fill=(3,4,10,255))
    d.polygon([(x+20,460),(x+48,550),(x+67,588),(x+53,597),(x+10,550)], fill=(3,4,10,255))
    # blue light spilling from doorway
    glow = Image.new("RGBA",(W,H),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((130,175,320,500), fill=(68,110,174,24))
    glow=glow.filter(ImageFilter.GaussianBlur(30))
    im.alpha_composite(glow) if im.mode=="RGBA" else None

def draw_phone(im, t):
    d=ImageDraw.Draw(im,"RGBA")
    # bedside table
    d.polygon([(20,590),(430,570),(450,800),(0,800)], fill=(20,14,18,255))
    d.line((0,625,450,605), fill=(91,63,53,110), width=4)
    # phone glow
    glow=Image.new("RGBA",(W,H),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((95,390,365,650), fill=(74,137,232,45))
    glow=glow.filter(ImageFilter.GaussianBlur(34))
    im.paste(Image.alpha_composite(im.convert("RGBA"),glow).convert("RGB"))
    d=ImageDraw.Draw(im,"RGBA")
    d.rounded_rectangle((145,380,305,650), radius=24, fill=(2,4,10,255), outline=(111,128,151,255), width=3)
    d.rounded_rectangle((156,397,294,632), radius=15, fill=(13,24,42,255))
    d.ellipse((195,435,255,495), fill=(105,151,208,220))
    centered(d,505,"MOM",SUB,(235,241,255,255))
    centered(d,538,"INCOMING CALL",font(11,True),(142,168,203,255))
    d.ellipse((170,580,215,625), fill=(142,42,54,255))
    d.ellipse((235,580,280,625), fill=(45,145,91,255))
    # phone screen pulse
    d.line((180,605,205,605), fill=(255,255,255,230), width=3)
    d.arc((244,591,271,617), 200, 330, fill=(255,255,255,240), width=3)

def vignette(im):
    overlay=Image.new("L",(W,H),0)
    p=overlay.load()
    for y in range(H):
        for x in range(W):
            dist=math.sqrt(((x-W/2)/(W*.72))**2+((y-H/2)/(H*.72))**2)
            p[x,y]=int(max(0,min(175,(dist-.42)*240)))
    black=Image.new("RGB",(W,H),(0,0,0))
    return Image.composite(black,im,overlay.filter(ImageFilter.GaussianBlur(8)))

def render_frame(i):
    t=i/FPS
    im=gradient(i//3)
    # Scene changes are deliberately paced for a 15-second short.
    if t < 3.0:
        draw_house(im,t)
    elif t < 7.0:
        draw_girl(im,t)
    elif t < 11.0:
        draw_phone(im,t)
    else:
        draw_house(im,t)
        # distant, ghostly figure in the upstairs window
        d=ImageDraw.Draw(im,"RGBA")
        d.ellipse((188,423,224,459), fill=(210,221,238,125))
        d.polygon([(184,454),(228,454),(242,535),(170,535)], fill=(186,201,222,85))
    im=vignette(im)
    # Subtle cinematic camera drift / shake.
    dx=int(math.sin(t*1.1)*4)
    im=im.transform((W,H),Image.Transform.AFFINE,(1,0,dx,0,1,0),resample=Image.Resampling.BICUBIC)
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle((0,0,W,68), fill=(0,0,0,110))
    d.text((20,22),"A MIDNIGHT MYSTERY",font=font(13,True),fill=(164,183,208,220))
    d.text((W-62,22),"01:13",font=font(13,True),fill=(164,183,208,200))
    if t < 2.5:
        centered(d,110,"THE GIRL WHO\nHEARD HER DEAD MOTHER",TITLE,(240,242,250,255),8)
        centered(d,220,"A SHORT MYSTERY FILM",SMALL,(173,194,224,255))
    elif 3.0 <= t < 7.0:
        if t < 4.4: centered(d,110,"“WHO'S THERE?”",SUB,(234,239,250,255))
        elif t < 6.0: centered(d,110,"A VOICE FROM THE DARK",SUB,(206,219,240,255))
        else: centered(d,110,"IT KNEW HER NAME.",SUB,(235,215,194,255))
    elif 7.0 <= t < 11.0:
        centered(d,115,"UNKNOWN CALLER",SMALL,(164,184,213,255))
    elif t < 13.0:
        centered(d,110,"MOM IS CALLING…",SUB,(237,240,248,255))
    else:
        # Final reveal with gentle fade-in.
        alpha=int(255*min(1,(t-13)/.8))
        centered(d,155,"SHE DIED",BIG,(255,230,230,alpha))
        centered(d,198,"THREE YEARS AGO.",BIG,(224,67,83,alpha))
        centered(d,265,"SO WHO IS CALLING HER?",SMALL,(204,215,233,alpha))
    # subtle film grain specks
    for _ in range(65):
        x=random.randrange(W); y=random.randrange(H)
        d.point((x,y), fill=(210,220,235,random.randrange(8,27)))
    return im

def main():
    frames_dir="frames"
    os.makedirs(frames_dir,exist_ok=True)
    for i in range(TOTAL):
        render_frame(i).save(f"{frames_dir}/frame_{i:04d}.jpg",quality=88)
        if i % 45 == 0:
            print(f"Rendered {i}/{TOTAL} frames", flush=True)
    # A low, eerie two-note drone, gently pulsing. No external audio files needed.
    subprocess.run([
        "ffmpeg","-y","-v","error",
        "-f","lavfi","-i",
        "sine=frequency=55:sample_rate=44100:duration=15",
        "-f","lavfi","-i",
        "sine=frequency=82.41:sample_rate=44100:duration=15",
        "-filter_complex",
        "[0:a]volume=0.13,afade=t=in:st=0:d=1,afade=t=out:st=13.8:d=1.2[a0];"
        "[1:a]volume=0.045,afade=t=in:st=2:d=2,afade=t=out:st=13:d=2[a1];"
        "[a0][a1]amix=inputs=2:normalize=0,alimiter=limit=0.85[a]",
        "-map","[a]","-c:a","aac","-b:a","128k","drone.m4a"
    ],check=True)
    subprocess.run([
        "ffmpeg","-y","-v","error",
        "-framerate",str(FPS),"-i",f"{frames_dir}/frame_%04d.jpg",
        "-i","drone.m4a","-t",str(DURATION),
        "-vf","scale=450:800,format=yuv420p",
        "-c:v","libx264","-preset","veryfast","-crf","22",
        "-c:a","aac","-b:a","128k","-shortest",
        "-movflags","+faststart",OUT
    ],check=True)
    print(f"Created {OUT}")

if __name__ == "__main__":
    main()
