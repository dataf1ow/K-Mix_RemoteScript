from _Framework.ModeSelectorComponent import ModeSelectorComponent
from ConfigurableButtonElement import ConfigurableButtonElement
from K_MixUtility import K_MixUtility
from MIDI import *

class SendModeSelector(ModeSelectorComponent, K_MixUtility):
	"""Class that selects between modes"""

	def __init__(self,mixer):
		ModeSelectorComponent.__init__(self)
		self._mixer = mixer
		self.set_mode_toggle(self.button(CHANNEL,AUX1_BUTTON))
		#self.update()
		

	def set_modes_buttons(self, buttons):
		#raise buttons == None or isinstance(buttons, tuple) or len(buttons) == self.number_of_modes() or AssertionError
		identify_sender = True
		for button in self._modes_buttons:
			button.remove_value_listener(self._mode_value)
			button.remove_value_listener(self._mode_release)
		self._modes_buttons = []
		if buttons != None:
			for button in buttons:
				#raise isinstance(button, ButtonElement) or AssertionError
				self._modes_buttons.append(button)
				button.add_value_listener(self._mode_value, identify_sender)
				button.add_value_listener(self._mode_release, identify_sender)
		self.set_mode(0)


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
	def update(self):
		super(SendModeSelector, self).update()
		for track in range(len(self._mixer._sliders)):
			self._mixer._sliders[track].send_value(0)
		if self._mode_index == 0:
			self._mixer.setup_tracks()
		elif self._mode_index == 1:
			self._mixer.setup_sends()


	def _toggle_value(self, value):
		index = self._mode_index
		if self._mixer.is_active == True:
			if value != 0:
				if index == 0:
					self.set_mode(1)
					self._mixer.send_mode = 1
				if index == 1:
					self.set_mode(0)
					self._mixer.send_mode = 0
		if value == 0:
			if index == 1:
				self._mode_toggle.send_value(1)

	def _mode_release(self, value):
		if value == 0:
			index = self._mode_index
			if index == 1:
				self._mode_toggle.send_value(1)
      