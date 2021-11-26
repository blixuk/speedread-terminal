# file: speedread-terminal/__main__.py

from speedread import SpeedRead
from command import Command
cmd = Command(description="SpeedRead")

@cmd.command(
	cmd.argument("-f", "--file", help="file to read"),
	cmd.argument("-w", "--wpm", help="words per minute"),
	cmd.argument("-p", "--pointer", help="set pointer (pipe, carrot, dot, bar, full, none)"),
	cmd.argument("-F", "--focus", action="store_true", help="use focus on word, highlighting center character"),
	cmd.argument("-d", "--delay", action="store_true",help="use word delay based on word length"),
	cmd.argument("-P", "--punctuation", action="store_true",help="use punctuation delay")
)
def main(self, args):
	'''SpeedRead'''

	pointer = 'none'
	words_per_minute = 250
	word_focus = False
	word_delay = False
	punctuation_delay = False

	if args.wpm:
		words_per_minute = args.wpm
	if args.pointer:
		pointer = args.pointer
	if args.focus:
		word_focus = args.focus
	if args.delay:
		word_delay = args.delay
	if args.punctuation:
		punctuation_delay = args.punctuation

	if args.file:
		SpeedRead(args.file, words_per_minute, pointer, word_focus, word_delay, punctuation_delay)
		
	else:
		print("No file specified")
		cmd.printHelp()

if __name__ == '__main__':
	cmd.parse()