from __future__ import with_statement

import Live
import time
import math

from _Framework.ControlSurface import ControlSurface
from FaderSelectorComponent import FaderSelectorComponent
from K_MixSession import K_MixSession

class K_Mix(ControlSurface):
	'''Our K Mix Class'''

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		with self.component_guard():
			self.setup_selector()
			self.setup_session()
			self.set_highlighting_session_component(self.session)

	def setup_selector(self):
		self.selector = FaderSelectorComponent(8,self)
		self._device_component = self.selector._device

	def setup_session(self):
		self.session = K_MixSession(8, 6)
		self.session.set_offsets(0,0)
		self.session.set_mixer(self.selector._mixer)
		self.session.set_mixer(self.selector._meters)
		self.session.update()