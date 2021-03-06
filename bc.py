from bs4 import BeautifulSoup
import re, json, requests, os, sys

class Download():

	def __init__(self, args):
		self.url = args.url
		self.directory = args.dir

	def downloadSong(self, songName, songLink):
		if songLink is not None:
			try:
				songB = requests.get(songLink, stream=True)
				with open(songName + '.mp3', 'wb') as file:
					for chunk in songB.iter_content(chunk_size=1024):
						if chunk:
							file.write(chunk)
				songB.close()

			except KeyboardInterrupt:
				print("\nInterrupt signal received. Exiting...")
				sys.exit(0)
			
			return 1

	def download(self):
		try:
			reHTML = requests.get(self.url)
			assert reHTML.status_code == 200

		except(requests.exceptions.ConnectionError):
			print ("\nConnection error")
			sys.exit(-2)
		except(AssertionError, requests.exceptions.MissingSchema):
			print ("\nInvalid URL. Exiting...")
			sys.exit(-3)
		except KeyboardInterrupt:
			print ("\nInterrupt signal received. Exiting...")
			sys.exit(0)
		parsedResponse = BeautifulSoup(reHTML.text, 'html.parser')
		artist = parsedResponse.find('meta', {'property':'og:site_name'})['content']
		title = parsedResponse.find('title')
		album = re.sub('<.*?>', '', str(title))
		album = re.sub('[|]', 'by', album)

		if self.directory is not None:
			if not os.path.isdir(self.directory):
				os.mkdir(self.directory)
				os.chdir(str(self.directory))

		if not os.path.isdir(album):
			os.mkdir(album)
		os.chdir(os.getcwd() + '//' + str(album))

		varJSON = re.search('trackinfo: \[.*\]', reHTML.text)
		varJSON = str(varJSON.group())
		songData = json.loads(varJSON.strip('trackinfo: '))
		trackNumber = 1
		print(" ". join([str(len(songData)), 'track(s) found. Connecting to stream...']))
		print("Saving to: " + os.getcwd())
		for song in songData:
			songName = " ".join([str(trackNumber) + '.', artist, '-', song['title']]) 
			songLink = song['file']['mp3-128']
			trackNumber +=1
			try:
				if self.downloadSong(songName, songLink):
					print("Downloading " + songName + '.mp3' + '  ...done.')
			except KeyboardInterrupt:
				print("\nInterrupt signal received. Exiting...")
				sys.exit(0)








		
