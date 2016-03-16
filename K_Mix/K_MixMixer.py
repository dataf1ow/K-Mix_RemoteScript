from _Framework.MixerComponent import MixerComponent
from K_MixUtility import K_MixUtility
from MIDI import *


#SLIDER_CHANNEL = 0

class K_MixMixer(MixerComponent, K_MixUtility):
	def __init__(self, num_tracks):
		MixerComponent.__init__(self, num_tracks)
		self.setup_mixer(num_tracks)


	def setup_mixer(self, num_tracks):
		for track in range(num_tracks):
			strip = self.channel_strip(track)
			strip.set_volume_control(self.encoder(SLIDER_CHANNEL,SLIDERS[track]))
		master_strip = self.master_strip()
		master_strip.set_volume_control(self.encoder(SLIDER_CHANNEL,MASTER))