from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from K_MixUtility import K_MixUtility
from MIDI import *
import math
from _Framework.Debug import debug_print

class VU_Mode(MixerComponent, K_MixUtility):
	def __init__(self, num_tracks, parent):
		MixerComponent.__init__(self, num_tracks)
		self._sliders = []
		self.sends = []
		self.select_buttons = []
		self._rotaries = []
		self._meters = []
		self.offset = parent._track_offset
		self.parent = parent
		self.master_track = None
		self._active = False

		self._master_level = 0
		self._track_levels = []
		self._tracks = []
		##self.setup(num_tracks)
		for track in range(num_tracks):
			self._sliders.append(self.encoder(CHANNEL,SLIDERS[track]))
			self.select_buttons.append(self.button(CHANNEL,SELECT_BUTTONS[track]))
		self._sliders = tuple(self._sliders)
		for index in range(4):
			self._rotaries.append(self.encoder(CHANNEL,ROTARIES[index]))

		self._master_fader = self.encoder(CHANNEL,MASTER_SLIDER)
		self._master_select = self.button(CHANNEL,MASTER_BUTTON)


	def _create_strip(self):
		return K_MixChannelStrip()

	def _setup(self, as_enabled, num_tracks):
		for track in range(num_tracks):
			strip = self.channel_strip(track)
			strip.set_VU_control(None)
			strip.set_select_button(None)
			strip.set_send_controls(None)
			strip.set_pan_control(None)
			self._sliders[track].send_value(0)

		self._master_fader.send_value(0)		
		self.master_strip().set_select_button(None)

		
		self.sends = []

		for index in range(3):
			self.sends.append(self._rotaries[index + 1])

		if as_enabled:
			if self._active == False:
				#active
				self._tracks = []
				self.master_track = self.master_strip()

				for track in range(num_tracks):
					#self._sliders[track].send_value(0)
					strip = self.channel_strip(track)
					if strip._track != None:
						if strip._track.has_audio_output:
							strip.set_VU_control(self._sliders[track])
							strip._track.add_output_meter_left_listener(strip.observe)
							self._tracks.append(strip)
				self.master_track.set_VU_control(self._master_fader)
				self.master_track._track.add_output_meter_left_listener(self.master_track.observe)
				self._master_fader.send_value(0)
				self._active = True
				self.update()
		else: 
			if self._active == True:
				#not active
				for track in range(len(self._tracks)):
					if self._tracks[track] != None:
						if self._tracks[track]._track.has_audio_output:
							self._tracks[track].set_VU_control(None)
							#if self._tracks[track]._track.output_meter_left_has_listener(strip.observe):
							self._tracks[track]._track.remove_output_meter_left_listener(self._tracks[track].observe)
							self._tracks[track] = None
				if self.master_track != None:
					self.master_track._track.remove_output_meter_left_listener(self.master_track.observe)
					self.master_track = None
				self._active = False
				self.update()

	def flush_LEDs(self, num_tracks):
		for track in range(num_tracks):
			self._sliders[track].send_value(0)

	def log_message(self, *message):
		""" Writes the given message into Live's main log file """
		message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
		console_message = 'LOG: ' + message
		if debug_print != None:
			debug_print(console_message)
		else:
			print console_message
		if self.parent._c_instance:
			self.parent._c_instance.log_message(message)
	

class K_MixChannelStrip(ChannelStripComponent):
	def __init__(self, *a, **k):
		super(K_MixChannelStrip, self).__init__(*a, **k)
		self.frames = [0.0] * 2
		self.scale = 127
		self.current_level = 0
		self.master = None
		self._VU_control = None

	def observe(self):
		if self.track.has_audio_output == True:
			new_frame = self.track.output_meter_left
			self.store_frame(new_frame)
			level = self.rms(self.frames)
			if level != self.current_level:
				self.set_leds(level)

	def store_frame(self,frame):
		self.frames.pop(0)
		self.frames.append(frame)

	def rms(self,frames):
		return math.sqrt(sum(frame*frame for frame in frames)/len(frames))
	
	def set_VU_control(self, slider):
		identify_sender = True
		if slider != None:
			self._VU_control = slider
			slider.add_value_listener(self._VU_value)
			self.update()
		else: 
			if self._VU_control != None:
				self._VU_control.remove_value_listener(self._VU_value)
			self._VU_control = None
			self.update() 

	def set_leds(self, level):
		if self._VU_control != None:
			self._VU_control.send_value(level * self.scale)

	def _VU_value(self, data):
		self._track.mixer_device.volume.value = float(data)/127.0

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
	
	