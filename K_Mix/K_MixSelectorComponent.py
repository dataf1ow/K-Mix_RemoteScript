from _Framework.ModeSelectorComponent import ModeSelectorComponent
from ConfigurableButtonElement import ConfigurableButtonElement
from K_MixUtility import K_MixUtility
from K_MixMixer import K_MixMixer
from K_MixDevice import K_MixDevice
from MIDI import *

class K_MixSelectorComponent(ModeSelectorComponent, K_MixUtility):
	"""Class that selects between modes"""

	def __init__(self, num_tracks, parent):
		ModeSelectorComponent.__init__(self)
		self._mixer = K_MixMixer(num_tracks)
		self._device = K_MixDevice(parent)
		self._buttons_to_use = [self.button(CHANNEL, VU_BUTTON), self.button(CHANNEL, FINE_BUTTON)]
		self._buttons_to_use = tuple(self._buttons_to_use)
		self._mode_index = 0
		self.set_modes_buttons(self._buttons_to_use)
		self.update()

	def set_modes_buttons(self, buttons):
		#raise buttons == None or isinstance(buttons, tuple) or len(buttons) == self.number_of_modes() or AssertionError
		identify_sender = True
		for button in self._modes_buttons:
			button.remove_value_listener(self._mode_value)

		self._modes_buttons = []
		if buttons != None:
			for button in buttons:
				#raise isinstance(button, ButtonElement) or AssertionError
				self._modes_buttons.append(button)
				button.add_value_listener(self._mode_value, identify_sender)
				button.add_value_listener(self._mode_release, identify_sender)

		self.set_mode(0)

	def number_of_modes(self):
		return 2

	def on_enabled_changed(self):
		self.update()

	def set_mode(self, mode):
		if not mode in range(self.number_of_modes()):
			raise AssertionError
			self._mode_index = mode
			self.update()

	def update(self):
		super(K_MixSelectorComponent, self).update()
		if self._mode_index == 0:
			self._device._setup(False)
			self._mixer._setup(True, 8)
		elif self._mode_index == 1:
			self._mixer._setup(False, 8)
			self._device._setup(True)
	
	def on_selected_track_changed(self):
		if self._mode_index == 1:
			track =  self.song().view.selected_track
			device_count = track.devices
			if len(device_count) != 0:
				if self._device.selected_device != self.song().view.selected_track.devices[0]: 
					self._device.selected_device = self.song().view.selected_track.devices[0]
					self._device.set_device(self._device.selected_device)
				self._mixer.on_selected_track_changed()
			else:
				self._mixer.on_selected_track_changed()
		elif self._mode_index == 0:
			return
			#self._mixer.on_selected_track_changed()
	
	def _mode_release(self, value, identify_sender):
		if value == 0:
			if self._mode_index == 0:
				self._modes_buttons[0].send_value(1)
				self._modes_buttons[1].send_value(0)
			elif self._mode_index == 1:
				self._modes_buttons[1].send_value(1)
				self._modes_buttons[0].send_value(0)


      