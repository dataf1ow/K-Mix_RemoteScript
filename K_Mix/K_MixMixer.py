from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from K_MixUtility import K_MixUtility
from MIDI import *

class K_MixMixer(MixerComponent, K_MixUtility):
	def __init__(self, num_tracks):
		MixerComponent.__init__(self, num_tracks)
		self.sends = []
		self.select_buttons = []
		self.setup(num_tracks)

	def _create_strip(self):
		return K_MixChannelStrip()

	def setup(self, num_tracks):
		for track in range(num_tracks):
			strip = self.channel_strip(track)
			strip.set_volume_control(self.encoder(CHANNEL,SLIDERS[track]))
			self.select_buttons.append(self.button(CHANNEL,SELECT_BUTTONS[track]))
			strip.set_select_button(self.select_buttons[track])
		for index in range(3):
			self.sends.append(self.encoder(CHANNEL, ROTARIES[index + 1]))
		self.selected_strip().set_send_controls(tuple(self.sends))
		self.selected_strip().set_pan_control(self.encoder(CHANNEL, ROTARIES[0]))
		master_strip = self.master_strip()
		master_strip.set_volume_control(self.encoder(CHANNEL,MASTER))

class K_MixChannelStrip(ChannelStripComponent):
	def __init__(self, *a, **k):
		super(K_MixChannelStrip, self).__init__(*a, **k)
		'''
		def make_button_slot(name):
			return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')

		self._track_select_button_slot = make_button_slot('track_select')
		'''

	def set_select_button(self, button):
		if button != self._select_button:
			self.reset_button_on_exchange(self._select_button)
			self._select_button = button
			self._select_button_slot.subject = button
			self._select_button.add_value_listener(self._select_release)
			self.update()

	def _select_release(self, value):
		if value == 0:
			if self._track != None and self.song().view.selected_track == self._track:
				self._select_button.send_value(1)
	