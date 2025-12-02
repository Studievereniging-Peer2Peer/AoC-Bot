# AoC Discord Bot Peer2Peer

Discord bot to interface the Advent of Code private leaderboard with Discord via commands.

## Commands

The current list of commands avaible in Discord

| Command | Description |
| - | - |
| ```&leaderboard``` | Show current top 20 on the leaderboard |

## Env variables

Er zijn een aantal env variables nodig om te kunnen werken:
- `DISCORD_TOKEN` - Dit is het token van de discord bot.
- `SESSION_ID` - The contents of the session cookie of a signed in account with access to the leaderboard
- `LEADERBOARD_URL` - De API url van het leaderboard, te vinden op de leaderboard pagina

## Setup guide:

For this program docker is required, if you haven't already, you can install it by executing the following commands (on Linux):

```sh
curl -fsSL https://get.docker.com | sudo bash
sudo systemctl start docker
sudo systemctl enable docker
```

Then to ge the program running, build using the container file

```sh
sudo docker build -t aoc-bot -f Containerfile .
```

And run it by replacing the 'xxx' and running the command:

```sh
sudo docker run -d --name aoc-bot \
  -e DISCORD_TOKEN=xxx \
  -e LEADERBOARD_URL=xxx \
  -e SESSION_ID=xxx \
  aoc-bot
```

If needed you can remove the program by executing the following commands:

```sh
sudo docker stop aoc-bot
sudo docker rm aoc-bot
```
