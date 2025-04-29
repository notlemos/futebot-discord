# <p align="center"> futebot </p>
  
<p align="center"> <img src="https://camo.githubusercontent.com/ec9ce3fcf3aea61be65eac063a698e48b02afc3eb6ee67e80edfd4605f38c720/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e20332d3337373641422e7376673f7374796c653d266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465" />  </p>

____

#  Features

-  Real-time update of the Brazilian league table
-  Information about games, transfers and team players
-  Sign command
-  Weather forecast
-  Spotify current music status
-  Random commands

# Starting
## Prerequisites
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/)
- [Bot-Account](https://discordpy.readthedocs.io/en/stable/discord.html)
# Installing 
1. Clone the bot repositore using git.
```bash
git clone https://github.com/notlemos/futebot-discord.git
```
2. Go to the directory.
```bash
cd futebot-discord
```
# Running
3. Make sure to fill the ```.env``` file.
4. Build the docker service aplication.
```bash
docker-compose up --build
```
# References
- [discord.py](https://discordpy.readthedocs.io/en/stable/index.html#): Discord API
- [Pillow](https://pillow.readthedocs.io/en/stable/): Python Imaging Library
- [TMBD](https://developer.themoviedb.org/docs/getting-started): TMDB API for infos about movies.
