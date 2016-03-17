from _Framework.MixerComponent import MixerComponent
from K_MixUtility import K_MixUtility
from MIDI import *

class K_MixMixer(MixerComponent, K_MixUtility):
	def __init__(self, num_tracks):
		MixerComponent.__init__(self, num_tracks)
		self.sends = []
		self.setup(num_tracks)


	def setup(self, num_tracks):
		for track in range(num_tracks):
			strip = self.channel_strip(track)
			strip.set_volume_control(self.encoder(CHANNEL,SLIDERS[track]))
			strip.set_select_button(self.button(CHANNEL,SELECT_BUTTONS[track]))
		for index in range(3):
			self.sends.append(self.encoder(CHANNEL, ROTARIES[index + 1]))
		self.selected_strip().set_send_controls(tuple(self.sends))
		self.selected_strip().set_pan_control(self.encoder(CHANNEL, ROTARIES[0]))
		master_strip = self.master_strip()
		master_strip.set_volume_control(self.encoder(CHANNEL,MASTER))