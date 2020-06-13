import vapoursynth as vs

core = vs.get_core()
src = core.ffms2.Source(source=r'G:\Dumbo.2019.1080p.Blu-ray.Remux.AVC.TrueHD.Atmos.7.1-SURFINBIRD.mkv')
out = core.std.Crop(src, 0, 0, 20, 20)
select = core.std.SelectEvery(out[8000:-15000], cycle=6000, offsets=range(10))
out = core.std.AssumeFPS(select, fpsnum=out.fps.numerator, fpsden=out.fps.denominator)

srcout=core.ffms2.Source(source=r'G:/25.mkv',threads=1)
import fvsfunc as fvf
out = fvf.Depth(out, 10)
out=core.vmaf.VMAF(out,srcout,ssim=True, ms_ssim=True, model=0,log_path=r'G:/25.mkv.json',log_fmt=1)
out.set_output()