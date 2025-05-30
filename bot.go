package main

import "github.com/bwmarrin/discordgo"

func StartBot(cfg Config) (s *discordgo.Session, err error) {
	s, err = discordgo.New(cfg.Bot.Token)
	if err != nil {
		return
	}

	err = s.Open()
	if err != nil {
		return
	}

	err = createCommands(s)
	if err != nil {
		return
	}

	addCommandHandlers(s)
	StartTracker(s, cfg)
	
	return
}

func StopBot(s *discordgo.Session) (err error) {
	err = deleteCommands(s)
	if err != nil {
		return
	}

	err = s.Close()
	return
}