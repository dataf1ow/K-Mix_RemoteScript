

import Live
import time
import math

#from _Framework.Debug import debug_print
from _Framework.ControlSurface import ControlSurface
from _Framework.MixerComponent import MixerComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group, Subject
from .K_MixSession import K_MixSession
from .SendModeSelector import SendModeSelector
from .VUModeSelector import VUModeSelector
from .DeviceSelector import DeviceSelector
from .Device_Mode import Device_Mode
from .Mix_Mode import Mix_Mode
from .K_MixUtility import K_MixUtility
from .MIDI import *
debug_print = None

class K_Mix(ControlSurface,K_MixUtility):
	'''Our K Mix Class'''

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		with self.component_guard():
			self.setup_mixer()
			self.setup_device()
			self.setup_send_selector()
			self.setup_VU_selector()
			self.setup_device_selector()
			self.setup_session()
			self.set_highlighting_session_component(self.session)
			self.register_slot(self.song().view.selected_track.view, self._on_selected_device_changed, 'selected_device')
			

	def log_message(self, *message):
		#""" Writes the given message into Live's main log file """
		message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
		console_message = 'LOG: ' + message
		if debug_print != None:
			debug_print(console_message)
		else:
			print(console_message)
		if self._c_instance:
			self._c_instance.log_message(message)

	def setup_session(self):
		self.session = K_MixSession(8, 6, self)
		self.session.set_offsets(0,0)
		self.session.set_mixer(self.mixer)
		self.session.update()

	def setup_device(self):
		self.device = Device_Mode(self)

	def setup_mixer(self):
		self.mixer = Mix_Mode(8,8,self)	
		self.mixer.setup_master(True)

	def setup_send_selector(self):
		self.send_selector = SendModeSelector(self.mixer)

	def setup_device_selector(self):
		self.device_selector = DeviceSelector(self.mixer,self.device)

	def setup_VU_selector(self):
		self.VU_selector = VUModeSelector(self.mixer)

	def _on_selected_device_changed(self):
		self.device.on_selected_device_changed()
