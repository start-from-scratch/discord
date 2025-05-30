package main

import (
	"fmt"

	"github.com/bwmarrin/discordgo"
)

var commandHandlers = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
	"ping": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
			Type: discordgo.InteractionResponseChannelMessageWithSource,
			Data: &discordgo.InteractionResponseData{
				Content: fmt.Sprintf("Pong! :ping_pong: %dms", s.HeartbeatLatency().Milliseconds()),
				Flags: 1 << 6,
			},
		})
	},
}

func addCommandHandlers(s *discordgo.Session) {
	s.AddHandler(func(discordSession *discordgo.Session, i *discordgo.InteractionCreate) {
		commandName := i.ApplicationCommandData().Name

		if h, ok := commandHandlers[commandName]; ok {
			h(discordSession, i)
		}

		commandsUsed.WithLabelValues(commandName).Inc()
	})
}