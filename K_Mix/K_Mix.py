from __future__ import with_statement

import Live
import time
import math

from _Framework.ControlSurface import ControlSurface
from K_MixMixer import K_MixMixer
from K_MixSession import K_MixSession

class K_Mix(ControlSurface):
	'''Our K Mix Class'''

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		with self.component_guard():
			self.setup_mixer()
			self.setup_session()
			self.set_highlighting_session_component(self.session)

	def setup_mixer(self):
		self.mixer = K_MixMixer(8)

	def setup_session(self):
		self.session = K_MixSession(8, 1)
		self.session.set_offsets(0,0)
		self.session.set_mixer(self.mixer)
		self.session.update()