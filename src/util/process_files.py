import sys
sys.path.insert(0, '../')
import textpreprocess

Process = textpreprocess.Process()

if __name__ == '__main__':
	Process.readAndProcessFiles()