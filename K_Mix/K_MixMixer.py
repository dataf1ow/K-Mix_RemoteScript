from _Framework.MixerComponent import MixerComponent
from K_MixUtility import K_MixUtility
from MIDI import *

class K_MixMixer(MixerComponent, K_MixUtility):
	def __init__(self, num_tracks):
		MixerComponent.__init__(self, num_tracks)
		self.setup(num_tracks)


	def setup(self, num_tracks):
		for track in range(num_tracks):
			strip = self.channel_strip(track)
			strip.set_volume_control(self.encoder(CHANNEL,SLIDERS[track]))
		master_strip = self.master_strip()
		master_strip.set_volume_control(self.encoder(CHANNEL,MASTER))