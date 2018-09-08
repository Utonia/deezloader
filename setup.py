from setuptools import setup
setup(
      name = "deezloader",
      version = "1.0",
      description = "Downloads songs, albums or playlists from deezer",
      license = "Apache-2.0",
      author = "An0nimia",
      author_email = "An0nimia@protonmail.com",
      packages = ["deezloader"],
      install_requires = ['mutagen', 'requests', 'spotipy', 'tqdm']
)