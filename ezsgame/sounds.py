from typing import Optional
from unittest.mock import DEFAULT
import pygame as pg

class Mixer:
    def __init__(self):
        if pg.mixer.get_init() is None:
            pg.mixer.init()
    
        self.sounds = []
        
    def __str__(self):
        return f"<Object: Mixer, ID : {self._id}>"

    def __repr__(self):
        return f"<Object: Mixer, ID : {self._id}>"
        
    def load(self, filename):
        self.sounds.append(Sound(filename))
        
    def _load_sound(self, sound_object):
        self.sounds.append(sound_object)

    def play(self):
        for sound in self.sounds:
            sound.play()

    def stop(self):
        for sound in self.sounds:
            sound.stop()
            
    def remove(self, sound):
        if sound in self.sounds:
            self.sounds.remove(sound)
        else:
            raise ValueError("Sound not in list")
     
    def clear(self):
        for sound in self.sounds:
            del sound
  
DEFAULT_MIXER = Mixer()

class Sound:
    def __init__(self, file, mixer: Mixer | None = None):
        try:
            self.sound = pg.mixer.Sound(file)
        except Exception as e:
            raise Exception(f"Could not load sound file <{file}>. \n Error: {e}")
        
        self.sound.set_volume(0.5)
        
        self.mixer = mixer or DEFAULT_MIXER
        
        self.mixer._load_sound(self)
        self.length = self.sound.get_length()
        
    @property
    def volume(self):
        return self.sound.get_volume()

    @volume.setter
    def volume(self, volume):
        self.sound.set_volume(volume)

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()
        
    def set_volume(self, volume):
        self.sound.set_volume(volume)
    
    def fadeout(self, time):
        self.sound.fadeout(time)
        
    def fadein(self, time):
        self.sound.fadein(time)
        
    def __str__(self):
        return f"<Object: Sound>"

    def __repr__(self):
        return f"<Object: Sound>"
    
    def __del__(self):
        if self in self.mixer.sounds:
            self.mixer.remove(self)
        del self.sound
        
    def raw(self):
        return self.sound.get_raw()