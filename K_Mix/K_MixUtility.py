from ConfigurableButtonElement import ConfigurableButtonElement
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement


class K_MixUtility(object):
  """ Provides some functionality shared across ALL classes """

  def button(self, channel, note):
    return ConfigurableButtonElement(True, MIDI_NOTE_TYPE, channel, note)

  def encoder(self, channel, cc):
    return SliderElement(MIDI_CC_TYPE, channel, cc)
