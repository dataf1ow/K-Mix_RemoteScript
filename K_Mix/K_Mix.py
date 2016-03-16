from __future__ import with_statement

import Live
import time
import math

from _Framework.ControlSurface import ControlSurface
from K_MixMixer import K_MixMixer

class K_Mix(ControlSurface):
	'''Our K Mix Class'''

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		with self.component_guard():
			self.setup_mixer()

	def setup_mixer(self):
		self.mixer = K_MixMixer(8)