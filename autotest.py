import json
import re
import os
import shutil
import sys
import time
import yaml

with open('setting.yaml', 'r') as f:
    set = yaml.load(f,Loader=yaml.FullLoader)
x265 = set["x265"]
vspipe = set["vspipe"]
setting = set['setting']
qcomp = setting['qcomp']
preset = setting['preset']
bframes = setting['bframes']
ctu = setting['ctu']
rd = setting['rd']
subme = setting['subme']
ref = setting['ref']
rclookahead = setting['rc-lookahead']
vbvbufsize = setting['vbv-bufsize']
vbvmaxrate = setting['vbv-maxrate']
colorprim = setting['colorprim']
transfer = setting['transfer']
colormatrix = setting['colormatrix']
deblock = setting['deblock']
ipratio = setting['ipratio']
pbratio = setting['pbratio']
aqmode = setting['aq-mode']
aqstrength = setting['aq-strength']
psyrd = setting['psy-rd']
psyrdoq = setting['psy-rdoq']


def testvmaf(vpy):
    pass


def testenconde(vpy, crf, savepath):
    script = f'{vspipe} "{vpy}" --y4m -i -'
    infol = os.popen(script)
    for i in infol:
        print(i)
        if i[0:6] == 'Frames':
            info = int(i.split(':')[1])
    ot = os.path.join(savepath, str(crf) + ".mkv")
    shell = f'{vspipe} "{vpy}" --y4m - | "{x265}" -D 10 --preset {preset} --crf {crf} --high-tier --ctu {ctu} --rd 4 ' \
            f'--subme {subme} --ref {ref} --pmode --no-rect --no-amp --rskip 0 --tu-intra-depth 4 --tu-inter-depth 4 --range limited ' \
            f'--no-open-gop --no-sao --rc-lookahead {rclookahead} --no-cutree --bframes {bframes} --vbv-bufsize {vbvbufsize} --vbv-maxrate {vbvmaxrate} ' \
            f'--colorprim bt709 --transfer bt709 --colormatrix bt709 --deblock {deblock} --ipratio {ipratio} --pbratio {pbratio} --qcomp {qcomp} ' \
            f'--aq-mode {aqmode} --aq-strength {aqstrength} --psy-rd {psyrd} --psy-rdoq {psyrdoq} --frames {info} --output "{ot}" --y4m - 2> "{os.path.join(savepath, "temp.txt")}"'
    print(shell)
    os.system(shell)
    with open(os.path.join(savepath, "temp.txt"), 'r') as f:
        wrline = []
        read = f.readlines()
        for i in read:
            if not re.search(r'\[\d+.*\%\]', i):
                wrline.append(i)
    with open('{ot}log.txt'.format(ot=ot), 'w') as f:
        f.writelines(wrline)
    return ot


def vmaf(vpy: str, mkv: str) -> float:
    outvpy = []
    pattern = re.compile(r'(\w*)\.set_output\(\)')
    with open(vpy, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not re.match(pattern, line):
                outvpy.append(line)
            else:
                res = re.match(pattern, line)
                setout = res.group(1)
                break
        outvpy.append(f"srcout=core.ffms2.Source(source=r'{mkv}',threads=1)\n")
        outvpy.append(f"import fvsfunc as fvf\n"
                      f"{setout} = fvf.Depth({setout}, 10)\n")
        outvpy.append(
            f"out=core.vmaf.VMAF({setout},srcout,ssim=True, ms_ssim=True, model=0,log_path=r'{mkv}.json',log_fmt=1)\n")
        outvpy.append(r'out.set_output()')
    with open('temp.vpy','w') as f:
        f.writelines(outvpy)
    shell = f'{vspipe} "temp.vpy" .'
    os.system(shell)
    with open(f"{mkv}.json", 'r') as f:
        vmafjs = json.load(f)
        vmafscore=vmafjs.get("VMAF score")
    return float(vmafscore)


if __name__ == '__main__':
    VS = input("脚本文件")
    VS='G:/1234567/v.vpy'
    savePath = os.path.split(VS)[0]
    ot=testenconde(VS,21,savePath)
    vmaf(VS,ot)

