from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from K_MixUtility import K_MixUtility
from MIDI import *
import math
from _Framework.Debug import debug_print


class Mix_Mode(MixerComponent,K_MixUtility):
	def __init__(self,num_tracks,num_returns,parent):
		self._is_active = False
		MixerComponent.__init__(self,num_tracks,num_returns)		
		self.parent = parent
		self.num_tracks = num_tracks
		self._sliders = []                                       
		self._sends = []
		self._select_buttons = []
		self._rotaries = []
		self.VU_mode = 0
		self.send_mode = 0
		self.is_active = True
		#self.device = device
		self._master_fader = self.encoder(CHANNEL,MASTER_SLIDER)
		self._master_select = self.button(CHANNEL,MASTER_BUTTON)

		for track in range(num_tracks):
			self._sliders.append(self.encoder(CHANNEL,SLIDERS[track]))

		for index in range(4):
			self._rotaries.append(self.encoder(CHANNEL,ROTARIES[index]))

		for track in range(num_tracks):
			self._select_buttons.append(self.button(CHANNEL,SELECT_BUTTONS[track]))
		self._is_active = True
		

	def _create_strip(self):
		return K_MixChannelStrip()
	
	def setup_master(self,as_enabled = True):	
		if as_enabled:
			for index in range(3):
				self._sends.append(self._rotaries[index + 1])
			self.selected_strip().set_send_controls(tuple(self._sends))
			self.selected_strip().set_pan_control(self._rotaries[0])
			self.master_strip().set_select_button(self._master_select)
			self.master_strip().set_volume_control(self._master_fader)

	def setup(self, is_active):
		self.is_active = is_active
		if self.is_active == True: 
			self.setup_sliders()
		if self.is_active == False: 
			for track in range(self.num_tracks):
				if self._sliders[track] != None:
					self._sliders[track].send_value(0)
				strip = self.channel_strip(track)
				return_strip = self.return_strip(track)
				if strip._volume_control != None:
					strip.set_volume_control(None)
				if strip._VU_control != None: 
					strip.set_VU_control(None)


	def setup_tracks(self):
		for track in range(self.num_tracks):
			strip = self.channel_strip(track)
			return_strip = self.return_strip(track)
			return_strip.set_select_button(None)
			strip.set_select_button(self._select_buttons[track])
			if self.VU_mode == 0:
				return_strip.set_volume_control(None)
				strip.set_volume_control(self._sliders[track])
			if self.VU_mode == 1:
				return_strip.set_VU_control(None)
				strip.set_VU_control(self._sliders[track])
			self.update()

	def setup_sends(self):
		for track in range(self.num_tracks):
			strip = self.channel_strip(track)
			return_strip = self.return_strip(track)
			strip.set_select_button(None)
			return_strip.set_select_button(self._select_buttons[track])
			if self.VU_mode == 0:
				strip.set_volume_control(None)
				return_strip.set_volume_control(self._sliders[track])
			if self.VU_mode == 1:
				strip.set_VU_control(None)
				return_strip.set_VU_control(self._sliders[track])
			self.update()

	def setup_sliders(self):
		for track in range(self.num_tracks):
			if self._sliders[track] != None:
				self._sliders[track].send_value(0)
			strip = self.channel_strip(track)
			return_strip = self.return_strip(track)
			if self.send_mode == 0:
				if strip._volume_control != None:
					strip.set_volume_control(None)
				if strip._VU_control != None: 
					strip.set_VU_control(None)
				self.setup_tracks()
			if self.send_mode == 1:
				if return_strip._volume_control != None:
					return_strip.set_volume_control(None)
				if return_strip._VU_control != None: 
					return_strip.set_VU_control(None)
				self.setup_sends()
		if self.VU_mode == 0:
			self.master_strip().set_VU_control(None)
			self.master_strip().set_volume_control(self._master_fader)
		if self.VU_mode == 1:
			self.master_strip().set_volume_control(None)
			self.master_strip().set_VU_control(self._master_fader)
			

	def flush_LEDs(self, num_tracks):
		for track in range(num_tracks):
			self._sliders[track].send_value(0)

	def _reassign_tracks(self):
		super(Mix_Mode,self)._reassign_tracks()
		if self._is_active == True:
			for track in range(self.num_tracks):
				strip = self.channel_strip(track)
				selected_track = self.song().view.selected_track
				if strip._track == selected_track:
					self._select_buttons[track].send_value(1)
				if track > len(self.song().visible_tracks) - self._track_offset - 1:
					self._sliders[track].send_value(0)


	def restore_sliders(self,num_tracks):
		for track in range(num_tracks):
			value_to_send = self._sliders[track].value
			self._sliders[track].send_value(value_to_send)

	def log_message(self, *message):
		#""" Writes the given message into Live's main log file """
		message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
		console_message = 'LOG: ' + message
		if debug_print != None:
			debug_print(console_message)
		else:
			print console_message
		if self.parent._c_instance:
			self.parent._c_instance.log_message(message)

	def on_track_list_changed(self):
		super(Mix_Mode,self).on_track_list_changed()


class K_MixChannelStrip(ChannelStripComponent):
	def __init__(self, *a, **k):
		super(K_MixChannelStrip, self).__init__(*a, **k)
	
		self.frames = [0.0] * 2
		self.scale = 127
		self.current_level = 0
		self.master = None
		self._VU_control = None

	def observe(self):
		if self._track != None:	
			if self._track.has_audio_output == True:
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
	
	def set_VU_control(self,slider):
		identify_sender = True
		if slider != None:
			self._VU_control = slider
			slider.add_value_listener(self._VU_value)
			if self._track != None:
				if self._track.has_audio_output:
					if not self._track.output_meter_left_has_listener(self.observe):
						self._track.add_output_meter_left_listener(self.observe)
			self.update()
		else: 
			if self._VU_control != None:
				self._VU_control.remove_value_listener(self._VU_value)
			self._VU_control = None
			if self._track != None:
				if self._track.has_audio_output:
					if self._track.output_meter_left_has_listener(self.observe):
						self._track.remove_output_meter_left_listener(self.observe)
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
				self.update()
		if button == None:
			self.reset_button_on_exchange(self._select_button)
			self._select_button = button
			self._select_button_slot.subject = button
			self.update()

	def _select_value(self, value):
		super(K_MixChannelStrip,self)._select_value(value)
		if value == 0:
			if self._track != None and self.song().view.selected_track == self._track:
				self._select_button.send_value(1)

	
