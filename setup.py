from setuptools import setup
setup(
      name = "deezloader",
      version = "1.2",
      description = "Downloads songs, albums or playlists from deezer",
      license = "Apache-2.0",
      author = "An0nimia",
      author_email = "An0nimia@protonmail.com",
      packages = ["deezloader"],
      install_requires = ['bs4', 'mutagen', 'requests', 'spotipy', 'tqdm']
)