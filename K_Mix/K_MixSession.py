from _Framework.SessionComponent import SessionComponent
from K_MixUtility import K_MixUtility
from MIDI import *

class K_MixSession(SessionComponent, K_MixUtility):
	def __init__(self, num_tracks, num_scenes):
		SessionComponent.__init__(self, num_tracks, num_scenes)
		self.sends = ROTARIES[1:]
		self.setup(num_scenes)

	def setup(self,num_scenes):
		self.set_scene_bank_buttons(
			self.button(CHANNEL, STOP_BUTTON),
			self.button(CHANNEL, RECORD_BUTTON))

		self.set_track_bank_buttons(
			self.button(CHANNEL, PLAY_BUTTON),
			self.button(CHANNEL, REWIND_BUTTON))

		for scenes in range(num_scenes):
			self.scene(scenes).set_launch_button(self.button(CHANNEL, SCENE_LAUNCH_BUTTONS[scenes]))