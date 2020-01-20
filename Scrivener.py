import importlib.util, sys

g_isColorama = False
try:
	Colorama = importlib.import_module('colorama')
	g_isColorama = True
except:
	print("Colorama is not available.")

import logging
from atexit import register
from enum import IntEnum

class _Scrivener():
	class MessageLevel(IntEnum):
		NONE = 0
		DEBUG = 10
		INFO = 20
		SUCCESS = 21
		WARNING = 30
		ERROR = 40
		CRITICAL = 50
		EXCEPTION = 51
	
	_isLogging = False
	_isVerbose = False
	_isQuiet = False
	_isSilent = False
	_Log_Format = '{asctime}-15s {message}s'
	_Message_Format = '{}: {}'
	
	def _InitializeLogs(self, fileName):
		logging.basicConfig(filename=fileName, format=self._Log_Format, style='{', level=self.MessageLevel.INFO)
		self._logger = logging.getLogger(__name__)
		self._isLogging = True
	
	def _LogLine(self, mLvl, text):
		if self._isLogging:
			if mLvl == self.MessageLevel.DEBUG:
				self._logger.debug(text)
			if mLvl == self.MessageLevel.WARNING:
				self._logger.warning(text)
			if mLvl == self.MessageLevel.ERROR:
				self._logger.error(text)
			if mLvl == self.MessageLevel.EXCEPTION:
				self._logger.exception(text)
			else:
				self._logger.log(text)
	
	def _Print(self, mLvl, text):
		if mLvl == self.MessageLevel.NONE:
			print(text)
		else:
			print(self._Message_Format.format(mLvl, text))
	
	def _ProcessLine(self, mLvl, text):
		if self._isLogging:
			self._LogLine(mLvl, text)
		if not self._isSilent:
			self._Print(mLvl, text)
	
	def log(self, text):
		self._ProcessLine(self.MessageLevel.NONE, text)
	def info(self, text):
		self._ProcessLine(self.MessageLevel.INFO, text)
	def debug(self, text):
		self._ProcessLine(self.MessageLevel.DEBUG, text)
	def success(self, text):
		self._ProcessLine(self.MessageLevel.SUCCESS, text)
	def warning(self, text):
		self._ProcessLine(self.MessageLevel.WARNING, text)
	def error(self, text):
		self._ProcessLine(self.MessageLevel.ERROR, text)
	def exception(self, text):
		self._ProcessLine(self.MessageLevel.EXCEPTION, text)
	
	def AddArgParserArgs(self, parser):
		if 'argparse' in sys.modules:
			parser.add_arguments('-l', '--log', dest='logLoc', type=str, help='Create a log file at the provided location.', default=None)
			parser.add_arguments('-v', '--verbose', dest='isVerbose', action='store_true', help='Print all log levels.')
			parser.add_arguments('-q', '--quiet', dest='isQuiet', action='store_true', help='Print only error messages.')
			parser.add_arguments('-s', '--silent', dest='isSilent', action='store_true', help='Do not print anything (does not affect writing logs, if supplied.')
		else:
			raise NotImplementedError("AddArgParserArgs requires argparse to be imported.")

	def ProcessArgs(self, args):
		if args.logLoc:
			self._InitializeLogs(args.logLoc)
		
		if args.isVerbose and args.isQuiet:
			self._isVerbose = True
		elif args.isVerbose:
			self._isVerbose = True
		elif args.isQuiet:
			self._isQuiet = True
			
		if args.isSilent:
			self._isSilent = True

class _Scrivener_Color(_Scrivener):
	def __init__(self):
		Colorama.init(autoreset=True)
		register(self._Destroy)
	
	def _Destroy(self):
		Colorama.deinit()
	
	def _Print(self, mLvl, text):
		if mLvl == self.MessageLevel.DEBUG:
			print(Colorama.Style.BRIGHT + Colorama.Fore.BLUE + Colorama.Back.BLACK + text)
		elif mLvl == self.MessageLevel.SUCCESS:
			print(Colorama.Fore.GREEN + Colorama.Back.BLACK + text)
		elif mLvl == self.MessageLevel.WARNING:
			print(Colorama.Fore.YELLOW + Colorama.Back.BLACK + text)
		elif mLvl == self.MessageLevel.ERROR:
			print(Colorama.Fore.RED + Colorama.Back.BLACK + text)
		elif mLvl == self.MessageLevel.EXCEPTION:
			print(Colorama.Fore.RED + Colorama.Back.YELLOW + text)
		else:
			print(text)

if __name__ != "__main__":
	print("Scrivener is meant to be used as a submodule and not a script.")
else:
	if g_isColorama:
		Scrivener = _Scrivener_Color()
	else:
		Scrivener = _Scrivener()
	
	Scrivener.log("Log")
	Scrivener.debug("Debug")
	Scrivener.info("Info")
	Scrivener.success("Success")
	Scrivener.warning("Warning")
	Scrivener.error("Error")
	Scrivener.exception("Exception")
