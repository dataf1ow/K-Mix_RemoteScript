from _Framework.SessionComponent import SessionComponent
from K_MixUtility import K_MixUtility
from MIDI import *

class K_MixSession(SessionComponent, K_MixUtility):
	def __init__(self, num_tracks, num_scenes):
		SessionComponent.__init__(self, num_tracks, num_scenes)
		self.sends = ROTARIES[1:]
		self.setup()

	def setup(self):
		self.set_scene_bank_buttons(
			self.button(CHANNEL, SESSION_DOWN),
			self.button(CHANNEL, SESSION_UP))

		self.set_track_bank_buttons(
			self.button(CHANNEL, SESSION_RIGHT),
			self.button(CHANNEL, SESSION_LEFT))
