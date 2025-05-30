package main

import "github.com/bwmarrin/discordgo"

var commands = []*discordgo.ApplicationCommand{
	{
		Name: "ping",
		Description: "Donne la latence du bot",
	},
}

func createCommands(s *discordgo.Session) (err error) {
	for _, v := range commands {
		_, err = s.ApplicationCommandCreate(s.State.User.ID, "", v)
		if err != nil {
			return
		}
	}

	return
}

func deleteCommands(s *discordgo.Session) (err error) {
	for _, v := range commands {
		err = s.ApplicationCommandDelete(s.State.User.ID, "", v.ID)
		if err != nil {
			return
		}
	}

	return
}