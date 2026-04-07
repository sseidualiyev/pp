import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith(".wav") or f.endswith(".mp3")]
        self.index = 0
        self.is_playing = False

    def play(self):
        if not self.playlist:
            return

        track = os.path.join(self.music_folder, self.playlist[self.index])
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if not self.playlist:
            return

        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def previous(self):
        if not self.playlist:
            return

        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks"
        return self.playlist[self.index]