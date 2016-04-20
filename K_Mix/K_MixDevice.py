from _Framework.DeviceComponent import DeviceComponent 
from K_MixUtility import K_MixUtility
from MIDI import *

class K_MixDevice(DeviceComponent,K_MixUtility):
	def __init__(self, *a, **k):
		super(K_MixDevice, self).__init__(*a, **k)
		self.encoders = []
		self.selected_device = None

		for index in range(8):
			self.encoders.append(self.encoder(CHANNEL, SLIDERS[index]))

	def _setup(self, as_enabled):
		if self.selected_device != self.song().view.selected_track.view.selected_device:
			self.selected_device = self.song().view.selected_track.view.selected_device 
		self.set_device(self.selected_device)
		#device = DeviceComponent()
    	#self.set_device_component(device)
    	#device.set_parameter_controls(self._sliders)
		if as_enabled:
			self.set_parameter_controls(self.encoders)
			self.update()
		else:
			self.set_parameter_controls(None)

