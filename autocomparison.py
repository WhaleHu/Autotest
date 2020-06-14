import vapoursynth as vs
import random
import os
import mvsfunc as mvf

core = vs.get_core()


def FrameInfo(clip, title,
              style="sans-serif,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"):
    import functools
    def FrameProps(n, clip):
        clip = core.sub.Subtitle(clip, "Frame " + str(n) + " of " + str(
            clip.num_frames) + "\nPicture type: " + clip.get_frame(n).props._PictType.decode(), style=style)
        return clip

    clip = core.std.FrameEval(clip, functools.partial(FrameProps, clip=clip))
    clip = core.sub.Subtitle(clip, ['\n \n \n' + title], style=style)
    return clip


def compare(sclip, eclip, savepath, numb=12, Title='Encode',
            style="sans-serif,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"):
    os.makedirs(savepath, exist_ok=True)
    flist = []
    while len(flist) < numb:
        num = abs(len(flist) - numb)
        start = int(len(sclip) * random.random() * 0.06 + 0.05)
        end = int(len(sclip) * (random.random() * 0.1 + 0.8))
        farmlist = range(start, end, int((end - start) / num))
        for i in farmlist:
            if not eclip.get_frame(i).props._PictType.decode() == 'B':
                continue
            if sclip.get_frame(i).props._PictType.decode() == 'I':
                continue
            flist.append(i)
    sclip = FrameInfo(sclip, 'Source')
    eclip = FrameInfo(eclip, Title, style=style)
    sclip = mvf.ToRGB(sclip)
    eclip = mvf.ToRGB(eclip)
    sclip = core.imwri.Write(sclip, "png", os.path.join(savepath, '%d-A.png'), overwrite=True)
    eclip = core.imwri.Write(eclip, "png", os.path.join(savepath, '%d-B.png'), overwrite=True)
    print(flist)
    for i in flist:
        print('正在截图第%d帧' % i)
        sclip.get_frame(i)
        eclip.get_frame(i)
    return eclip


def comparelist(sclip, eclip, savepath, numb=12, Title='Encode',
                style="sans-serif,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"):
    os.makedirs(savepath, exist_ok=True)
    flist = []
    while len(flist) < numb:
        num = abs(len(flist) - numb)
        start = int(len(sclip) * random.random() * 0.06 + 0.05)
        end = int(len(sclip) * (random.random() * 0.1 + 0.8))
        farmlist = range(start, end, int((end - start) / num))
        for i in farmlist:
            if not eclip[1].get_frame(i).props._PictType.decode() == 'B':
                continue
            if sclip.get_frame(i).props._PictType.decode() == 'I':
                continue
            flist.append(i)
    sclip = FrameInfo(sclip, 'Source')
    sclip = mvf.ToRGB(sclip)
    sclip = core.imwri.Write(sclip, "png", os.path.join(savepath, '%d-A.png'), overwrite=True)
    for i in flist:
        sclip.get_frame(i)
    ecn = 0
    for ec in eclip:
        ec = FrameInfo(ec, Title, style=style)
        ec = mvf.ToRGB(ec)
        ec = core.imwri.Write(ec, "png", os.path.join(savepath, f'%d-B-{ecn}.png'), overwrite=True)
        for i in flist:
            ec.get_frame(i)
        ecn = ecn + 1
    return eclip
