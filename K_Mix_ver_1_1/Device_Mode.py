from _Framework.DeviceComponent import DeviceComponent 
from K_MixUtility import K_MixUtility
from MIDI import *
from _Framework.Debug import debug_print
from _Framework.SubjectSlot import subject_slot, subject_slot_group, Subject


def device_to_appoint(device):
	appointed_device = device
	if device != None and device.can_have_drum_pads and not device.has_macro_mappings and len(device.chains) > 0 and device.view.selected_chain != None and len(device.view.selected_chain.devices) > 0:
		appointed_device = device_to_appoint(device.view.selected_chain.devices[0])
	return appointed_device


class Device_Mode(DeviceComponent,K_MixUtility):
	def __init__(self, parent, *a, **k):
		super(Device_Mode, self).__init__(*a, **k)
		self.encoders = []
		self._device_left_button = None
		self._device_right_button = None
		self.selected_device = None
		self.parent = parent
		self.track = None
		self._active = False

		def make_button_slot(name):
			return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')

		for index in range(8):
			self.encoders.append(self.encoder(CHANNEL, SLIDERS[index]))


		self._device_left_slot = make_button_slot('device_left')
		self._device_right_slot = make_button_slot('device_right')

	def set_device_left_button(self, button):
		if button != None:
			if button != self._device_left_button:
				self._device_left_button = button
				self._device_left_slot.subject = button
	
	def set_device_right_button(self, button):
		if button != None:
			if button != self._device_right_button:
				self._device_right_button = button
				self._device_right_slot.subject = button

	def _device_right_value(self, value):
		if value == 127:
			count = 0	
			for device in self.song().view.selected_track.devices:
				if device == self.song().view.selected_track.view.selected_device:
					index = count
				count = count + 1
			if index + 1 == len(self.song().view.selected_track.devices):
				index = -1
			self.song().appointed_device = device_to_appoint(self.song().view.selected_track.devices[index + 1])
			self.song().view.select_device(self.song().view.selected_track.devices[index + 1], False)
			if self.selected_device != self.song().view.selected_track.view.selected_device:
				self.selected_device = self.song().view.selected_track.view.selected_device 
			self.set_device(self.selected_device)

	def _device_left_value(self, value):
		if value == 127:
			count = 0	
			for device in self.song().view.selected_track.devices:
				if device == self.song().view.selected_track.view.selected_device:
					index = count
				count = count + 1
			self.song().appointed_device = device_to_appoint(self.song().view.selected_track.devices[index - 1])
			self.song().view.select_device(self.song().view.selected_track.devices[index - 1], False)
			if self.selected_device != self.song().view.selected_track.view.selected_device:
				self.selected_device = self.song().view.selected_track.view.selected_device 
			self.set_device(self.selected_device)

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

	def on_selected_track_changed(self):
		track =  self.song().view.selected_track
		device_count = track.devices
		if len(device_count) != 0:
			if self.selected_device != self.song().view.selected_track.devices[0]: 
				self.song().view.select_device(self.song().view.selected_track.devices[0])
				self.selected_device = self.song().view.selected_track.devices[0]
		self.parent.mixer.on_selected_track_changed()
		self.set_device(self.selected_device)

	def on_selected_device_changed(self):
		if self.selected_device != self.song().view.selected_track.view.selected_device:
			self.selected_device = self.song().view.selected_track.view.selected_device 
		self.set_device(self.selected_device)

	def setup(self, as_enabled):
		if self.selected_device != self.song().view.selected_track.view.selected_device:
			self.selected_device = self.song().view.selected_track.view.selected_device 
		self.set_device(self.selected_device)
		self.set_parameter_controls(None)

		for slider in range(8):
			self.encoders[slider].send_value(0)
		#device = DeviceComponent()
    	#self.set_device_component(device)
    	#device.set_parameter_controls(self._sliders)
		if as_enabled:
			if self._active == False:
				self.set_parameter_controls(None)
				for slider in range(8):
					self.encoders[slider].send_value(0)
				self.set_parameter_controls(self.encoders)
				self.set_device_left_button(self.button(CHANNEL, HEADPHONE_BUTTON))
				self.set_device_right_button(self.button(CHANNEL,TRIM_BUTTON))
				self.set_bank_nav_buttons(self.button(CHANNEL, EQ_BUTTON), self.button(CHANNEL, GATE_BUTTON))
				self._active = True
				self.update()
		else:
			if self._active == True:
				self.set_parameter_controls(None)
				for slider in range(8):
					self.encoders[slider].send_value(0)
				self.set_device_left_button(None)
				self.set_device_right_button(None)
				self.set_bank_nav_buttons(None, None)
				self._active = False
				self.update()

