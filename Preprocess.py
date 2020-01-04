import numpy
from scipy.io import wavfile
from scipy.fftpack import dct
import matplotlib.pyplot as plt

class preporcess:
    def __init__(self,inpath,outpath):
        self.inpath=inpath
        self.outpath=outpath
        self.pre_emphasis=0.97
        self.frame_stride=0.01
        self.frame_size=0.025

    def get_signal(self):
        if self.path.endswith('.wav'):
            sample_rate, signal=wavfile.read(self.path)
            signal=signal[0:int(3.5*sample_rate)] #读取前3.5s 的数据
            return sample_rate,signal

    def pre_empasis(self,signal):
        """
        Pre-Emphasis 预加重
        第一步是对信号应用预加重滤波器，以放大高频。 预加重滤波器在几种方面有用：
        （1）平衡频谱，因为高频通常比低频具有较小的幅度；
        （2）避免在傅立叶变换操作期间出现数值问题；
        （3）还可改善信号 噪声比（SNR）。
        可以使用以下公式中的一阶滤波器将预加重滤波器应用于信号x：
                    y(t)=x(t) -αx(t-1)
        使用以下代码行即可轻松实现，其中滤波器系数（α）的典型值为0.95或0.97，
        """
        emphasized_signal = numpy.append(signal[0], signal[1:] - self.pre_emphasis * signal[:-1])
        return emphasized_signal

    def get_frame(self,emphasized_signal):
        """
        经过预加重后，我们需要将信号分成短帧。 此步骤的基本原理是信号中的频率会随时间变化，
        因此在大多数情况下，对整个信号进行傅立叶变换是没有意义的，
        因为我们会随时间丢失信号的频率轮廓。
        为避免这种情况，我们可以假设信号的频率在很短的时间内是固定的。
        因此，通过在此短帧上进行傅立叶变换，可以通过串联相邻帧来获得信号频率轮廓较好的近似。
        语音处理中的典型帧大小为20毫秒至40毫秒，连续帧之间有50％（+/- 10％）重叠。
        常见的设置是帧大小为25毫秒，frame_size = 0.025和10毫秒跨度（重叠15毫秒），
        """
        frame_length, frame_step = self.frame_size * self.sample_rate, self.frame_stride * self.sample_rate  # Convert from seconds to samples
        signal_length = len(emphasized_signal)
        frame_length = int(round(frame_length))
        frame_step = int(round(frame_step))
        num_frames = int(numpy.ceil(
            float(numpy.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame

        pad_signal_length = num_frames * frame_step + frame_length
        z = numpy.zeros((pad_signal_length - signal_length))
        pad_signal = numpy.append(emphasized_signal, z)

        # 填充信号以确保所有帧具有相同数量的样本，而不会截断原始信号中的任何样本
        indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) + numpy.tile(
            numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
        frames = pad_signal[indices.astype(numpy.int32, copy=False)]
        return frame_length,frames

    def hamming_windows(self,frame_length,frames):
        """
        将信号切成帧后，我们对每个帧应用诸如汉明窗之类的窗口函数。 Hamming窗口具有以下形式：
                    w[n]=0.54-0.46cos(2*pi*n/(N-1))
        其中0<=n<=N-1, N是窗长
        有很多原因需要将窗函数应用于这些帧，特别是要抵消FFT无限计算并减少频谱泄漏
        """
        frames *= numpy.hamming(frame_length)
        # frames *= 0.54 - 0.46 * numpy.cos((2 * numpy.pi * n) / (frame_length - 1))  # Explicit Implementation **


    def get_figture(self,signal):
        axis_x = numpy.arange(0, signal.size, 1)
        plt.plot(axis_x, signal, linewidth=5)
        plt.title("Time domain plot")
        plt.xlabel("Time", fontsize=14)
        plt.ylabel("Amplitude", fontsize=14)
        plt.tick_params(axis='both', labelsize=14)
        plt.savefig(self.outpath)
        plt.show()
