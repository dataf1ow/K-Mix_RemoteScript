from _Framework.ModeSelectorComponent import ModeSelectorComponent
from .ConfigurableButtonElement import ConfigurableButtonElement
from .K_MixUtility import K_MixUtility
from .MIDI import *

class DeviceSelector(ModeSelectorComponent, K_MixUtility):
	"""Class that selects between modes"""

	def __init__(self,mixer,device):
		ModeSelectorComponent.__init__(self)
		self._mixer = mixer
		self._device = device
		self.set_mode_toggle(self.button(CHANNEL,FINE_BUTTON))
		#self.update()

	def set_mode_toggle(self, button):
		#if not (button == None or isinstance(button, ConfigurableButtonElement)):
		#	raise AssertionError
		if self._mode_toggle != None:
			self._mode_toggle.remove_value_listener(self._toggle_value)
			#self._mode_toggle.remove_value_listener(self._mode_release)
		self._mode_toggle = button
		self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)
		#self._mode_toggle.add_value_listener(self._mode_release)
		self.set_mode(0)

	def number_of_modes(self):
		return 2

	def on_enabled_changed(self):
		self.update()
	'''	
	def set_mode(self, mode):
		if mode < self.number_of_modes():
			self._mode_index = mode
			self.update()
	'''

	def _toggle_value(self, value):
		index = self._mode_index
		if value != 0:
			if index == 0:
				self.set_mode(1)
				self._mixer.setup(False)
				self._device.setup(True)
			if index == 1:
				self.set_mode(0)
				self._device.setup(False)
				self._mixer.setup(True)
		if value == 0:
			if index == 1:
				self._mode_toggle.send_value(1)

	def _mode_release(self, value):
		if value == 0:
			index = self._mode_index
			if index == 1:
				self._mode_toggle.send_value(1)
      