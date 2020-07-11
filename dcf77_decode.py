#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dcf77 Decode
# Generated: Sat Jul 11 17:15:34 2020
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import osmosdr
import time
import wx


class dcf77_decode(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Dcf77 Decode")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.sound_frequency = sound_frequency = 800
        self.samp_rate = samp_rate = 192000
        self.narrow_filter = narrow_filter = 200
        self.freq_adjust = freq_adjust = 77500
        self.decimation = decimation = 1
        self.audio_rate = audio_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        _volume_sizer = wx.BoxSizer(wx.VERTICAL)
        self._volume_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	label='Volume',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._volume_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_volume_sizer,
        	value=self.volume,
        	callback=self.set_volume,
        	minimum=0,
        	maximum=3,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_volume_sizer)
        _sound_frequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sound_frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sound_frequency_sizer,
        	value=self.sound_frequency,
        	callback=self.set_sound_frequency,
        	label='Sound frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._sound_frequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sound_frequency_sizer,
        	value=self.sound_frequency,
        	callback=self.set_sound_frequency,
        	minimum=400,
        	maximum=2000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_sound_frequency_sizer)
        _narrow_filter_sizer = wx.BoxSizer(wx.VERTICAL)
        self._narrow_filter_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_narrow_filter_sizer,
        	value=self.narrow_filter,
        	callback=self.set_narrow_filter,
        	label='Band Pass Width',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._narrow_filter_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_narrow_filter_sizer,
        	value=self.narrow_filter,
        	callback=self.set_narrow_filter,
        	minimum=10,
        	maximum=600,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_narrow_filter_sizer)
        _freq_adjust_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_adjust_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_adjust_sizer,
        	value=self.freq_adjust,
        	callback=self.set_freq_adjust,
        	label='Frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_adjust_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_adjust_sizer,
        	value=self.freq_adjust,
        	callback=self.set_freq_adjust,
        	minimum=10000,
        	maximum=1000000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_adjust_sizer)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=audio_rate,
        	fft_size=4096,
        	fft_rate=60,
        	average=False,
        	avg_alpha=None,
        	title='Audio frequency',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq_adjust,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title='Radio spectrum',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_clock_source('internal', 0)
        self.rtlsdr_source_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq_adjust, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(100, 0)
        self.rtlsdr_source_0.set_if_gain(200, 0)
        self.rtlsdr_source_0.set_bb_gain(200, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=audio_rate,
                decimation=samp_rate/decimation,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, freq_adjust+1000, 1000, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(1, (firdes.low_pass(1,samp_rate,samp_rate/(2*decimation), sound_frequency)), sound_frequency, samp_rate)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	3, samp_rate, sound_frequency-narrow_filter, sound_frequency+narrow_filter, sound_frequency, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(audio_rate, '', True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*120000/8.0))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.wxgui_fftsink2_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self._volume_slider.set_value(self.volume)
        self._volume_text_box.set_value(self.volume)
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_sound_frequency(self):
        return self.sound_frequency

    def set_sound_frequency(self, sound_frequency):
        self.sound_frequency = sound_frequency
        self._sound_frequency_slider.set_value(self.sound_frequency)
        self._sound_frequency_text_box.set_value(self.sound_frequency)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.sound_frequency)))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.sound_frequency)
        self.band_pass_filter_0.set_taps(firdes.band_pass(3, self.samp_rate, self.sound_frequency-self.narrow_filter, self.sound_frequency+self.narrow_filter, self.sound_frequency, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.freq_adjust+1000, 1000, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.sound_frequency)))
        self.band_pass_filter_0.set_taps(firdes.band_pass(3, self.samp_rate, self.sound_frequency-self.narrow_filter, self.sound_frequency+self.narrow_filter, self.sound_frequency, firdes.WIN_HAMMING, 6.76))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*120000/8.0))

    def get_narrow_filter(self):
        return self.narrow_filter

    def set_narrow_filter(self, narrow_filter):
        self.narrow_filter = narrow_filter
        self._narrow_filter_slider.set_value(self.narrow_filter)
        self._narrow_filter_text_box.set_value(self.narrow_filter)
        self.band_pass_filter_0.set_taps(firdes.band_pass(3, self.samp_rate, self.sound_frequency-self.narrow_filter, self.sound_frequency+self.narrow_filter, self.sound_frequency, firdes.WIN_HAMMING, 6.76))

    def get_freq_adjust(self):
        return self.freq_adjust

    def set_freq_adjust(self, freq_adjust):
        self.freq_adjust = freq_adjust
        self._freq_adjust_slider.set_value(self.freq_adjust)
        self._freq_adjust_text_box.set_value(self.freq_adjust)
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq_adjust)
        self.rtlsdr_source_0.set_center_freq(self.freq_adjust, 0)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.freq_adjust+1000, 1000, firdes.WIN_HAMMING, 6.76))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.sound_frequency)))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.wxgui_fftsink2_0_0.set_sample_rate(self.audio_rate)


def main(top_block_cls=dcf77_decode, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
