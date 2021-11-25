# file: speedread-terminal/speedread.py

import curses
import time
import os

class SpeedRead:

	def __init__(self, file:str, words_per_minute:int, pointer:str, word_focus:bool, word_delay:bool, punctuation_delay:bool) -> None:
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		curses.start_color()
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) # text colour RED and Background BLACK
		self.height, self.width = self.screen.getmaxyx()
		self.height_halved = int(self.height / 2)
		self.width_halved = int(self.width / 2)
		self.pointer_top, self.pointer_bottom = self.get_pointer(pointer)
		self.words_per_minute = words_per_minute
		self.word_focus = word_focus
		self.word_delay = word_delay
		self.punctuation_delay = punctuation_delay

		self.read(self.open_file(file))

	def read(self, file) -> None:
		try:
			for word in file.split():
				word_focus_index = self.get_word_index(word)
				self.screen.clear()
				self.screen.addstr(self.height_halved - 1, self.width_halved - 10, self.pointer_top) # ∨ # Added focus pointer top
				self.screen.addstr(self.height_halved, self.width_halved - word_focus_index, word)
				if self.word_focus: # Added RED colouring to focused character
					self.screen.addstr(self.height_halved, self.width_halved, word[word_focus_index], curses.color_pair(1) | curses.A_BOLD)
				self.screen.addstr(self.height_halved + 1, self.width_halved - 10, self.pointer_bottom) # ∧ # Added focus pointer bottom
				self.screen.move(0, 0)
				self.screen.refresh()
				time.sleep(self.get_word_delay(word))
		except KeyboardInterrupt:
			self.clean()
			exit()
		finally:
			self.clean()

	def clean(self):
		curses.nocbreak()
		curses.echo()
		curses.endwin()

	def get_word_index(self, word: str) -> int:
		word_length = len(word)
		if word_length <= 1:
			return 0
		elif 2 <= word_length <= 5:
			return 1
		elif 6 <= word_length <= 9:
			return 2
		elif 10 <= word_length <= 13:
			return 3
		else:
			return 4

	def get_word_delay(self, word: str) -> float:
		if self.word_delay:
			delay_factor = ((1 / float(self.words_per_minute) * 60) + (len(word) / 30))
		else:
			delay_factor =((1 / float(self.words_per_minute) * 60))

		punctuation_delay_factor = {',':2.0, ';':2.0, '...':5.0, '.':2.5, '!':2.5, ':':2.5, '?':3.0}
		if self.punctuation_delay:
			for punctuation in punctuation_delay_factor:
				if word.endswith(punctuation):
					return delay_factor * punctuation_delay_factor[punctuation]
			else:
				return delay_factor
		else:
			return delay_factor

	def get_pointer(self, pointer: str) -> list:
		if pointer == 'pipe':
			return '          |          ', '          |          '
		elif pointer == 'carrot':
			return '          ∨          ', '          ∧          '
		elif pointer == 'dot':
			return '          .          ', '          .          '
		elif pointer == 'bar':
			return '─────────────────────', '─────────────────────'
		elif pointer == 'full':
			return '──────────┬──────────', '──────────┴──────────'
		else:
			return  '', ''

	def open_file(self, file: str) -> str:
		if os.path.isfile(file):
			with open(file, 'r') as f:
				return f.read()
		else:
			self.clean()
			print(f"file not found: '{file}'")
			exit()