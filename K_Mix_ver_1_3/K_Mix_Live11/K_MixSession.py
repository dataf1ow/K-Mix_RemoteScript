from _Framework.SessionComponent import SessionComponent
from .K_MixUtility import K_MixUtility
from .MIDI import *
#from _Framework.Debug import debug_print

class K_MixSession(SessionComponent, K_MixUtility):
	def __init__(self, num_tracks, num_scenes,parent):
		SessionComponent.__init__(self, num_tracks, num_scenes)
		self.sends = ROTARIES[1:]
		self.setup(num_scenes)
		self.parent = parent
		debug_print = None

	def setup(self,num_scenes):
		self.set_scene_bank_buttons(
			self.button(CHANNEL, STOP_BUTTON),
			self.button(CHANNEL, RECORD_BUTTON))

		self.set_track_bank_buttons(
			self.button(CHANNEL, PLAY_BUTTON),
			self.button(CHANNEL, REWIND_BUTTON))

		for scenes in range(num_scenes):
			self.scene(scenes).set_launch_button(self.button(CHANNEL, SCENE_LAUNCH_BUTTONS[scenes]))

	def on_track_list_changed(self):
		super(K_MixSession,self).on_track_list_changed()

	def log_message(self, *message):
		#""" Writes the given message into Live's main log file """
		message = '(%s) %s' % (self.__class__.__name__, ' '.join(map(str, message)))
		console_message = 'LOG: ' + message
		if debug_print != None:
			debug_print(console_message)
		else:
			print(console_message)
		if self.parent._c_instance:
			self.parent._c_instance.log_message(message)