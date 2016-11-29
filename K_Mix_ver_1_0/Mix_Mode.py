from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from K_MixUtility import K_MixUtility
from MIDI import *

class Mix_Mode(MixerComponent, K_MixUtility):
	def __init__(self, num_tracks):
		MixerComponent.__init__(self, num_tracks)
		self._sliders = []                                       
		self.sends = []
		self._active = False
		self.select_buttons = []
		self._rotaries = []
		self._master_fader = self.encoder(CHANNEL,MASTER_SLIDER)
		self._master_select = self.button(CHANNEL,MASTER_BUTTON)
		##self.setup(num_tracks)
		for track in range(num_tracks):
			self._sliders.append(self.encoder(CHANNEL,SLIDERS[track]))

		for index in range(4):
			self._rotaries.append(self.encoder(CHANNEL,ROTARIES[index]))

		for track in range(num_tracks):
			self.select_buttons.append(self.button(CHANNEL,SELECT_BUTTONS[track]))



	def _create_strip(self):
		return K_MixChannelStrip()

	def _setup(self, as_enabled, num_tracks):
		for track in range(num_tracks):
			strip = self.channel_strip(track)
			strip.set_volume_control(None)
			strip.set_select_button(None)
			strip.set_send_controls(None)
			strip.set_pan_control(None)
		
		self.master_strip().set_volume_control(None)		
		self.master_strip().set_select_button(None)
		

		self.sends = []

		for index in range(3):
			self.sends.append(self._rotaries[index + 1])

		if as_enabled:
			if self._active == False:
				#active
				for track in range(num_tracks):
					self._sliders[track].send_value(0)
				for track in range(num_tracks):
					strip = self.channel_strip(track)
					strip.set_volume_control(self._sliders[track])
					strip.set_select_button(self.select_buttons[track])
				self.selected_strip().set_send_controls(tuple(self.sends))
				self.selected_strip().set_pan_control(self._rotaries[0])
				self.master_strip().set_volume_control(self._master_fader)
				self.master_strip().set_select_button(self._master_select)
				self._active = True
				self.update()
		else: 
			if self._active == True:
				#self.flush_LEDs(num_tracks)
				#not active
				for track in range(num_tracks):
					strip = self.channel_strip(track)
					strip.set_volume_control(None)
					strip.set_select_button(None)
				self.selected_strip().set_send_controls(None)
				self.selected_strip().set_pan_control(None)
				self.master_strip().set_volume_control(None)
				self.master_strip().set_select_button(self._master_select)	
				self._active = False
				self.update()

	def flush_LEDs(self, num_tracks):
		for track in range(num_tracks):
			self._sliders[track].send_value(0)

class K_MixChannelStrip(ChannelStripComponent):
	def __init__(self, *a, **k):
		super(K_MixChannelStrip, self).__init__(*a, **k)

	def set_select_button(self, button):
		if button != None:
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
	