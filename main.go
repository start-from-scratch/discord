package main 

import (
	"encoding/json"
	"os"
	"log"
	"os/signal"
	"fmt"

	"github.com/bwmarrin/discordgo"
)

type Config struct {
	Token string `json:"token"`
}

var config Config

func init() {
	raw, err := os.ReadFile("config.json")
  if err != nil {
    log.Println(err)
    return
  }
  err = json.Unmarshal(raw, &config)
	if err != nil {
    log.Fatalln(err)
  }
}

var s *discordgo.Session

func init() {
	var err error
	
	s, err = discordgo.New("Bot " + config.Token)
	if err != nil {
		log.Fatalf("Cannot create bot: %v", err)
	}
}

var (
	commands = []*discordgo.ApplicationCommand{
		{
			Name: "ping",
		},
	}

	commandHandlers = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
		"ping": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionResponseData{
					Content: fmt.Sprintf("Pong! :ping_pong: %dms", s.HeartbeatLatency().Milliseconds()),
				},
			})
		},
	}
)

func init() {
	s.AddHandler(func(discordSession *discordgo.Session, i *discordgo.InteractionCreate) {
		if h, ok := commandHandlers[i.ApplicationCommandData().Name]; ok {
			h(discordSession, i)
		}
	})
}

func main() {
	s.AddHandler(func(s *discordgo.Session, r *discordgo.Ready) {
		log.Printf("Logged in as %s", r.User.String())
	})
	err := s.Open()
	if err != nil {
		log.Fatalln(err)
	}

	log.Printf("Creating commands... (%d)", len(commands))
	registeredCommands := make([]*discordgo.ApplicationCommand, len(commands))
	for i, v := range commands {
		cmd, err := s.ApplicationCommandCreate(s.State.User.ID, "", v)
		if err != nil {
			log.Fatalf("Cannot create \"%v\" command: %v", v.Name, err)
		}
		registeredCommands[i] = cmd
	}
	defer s.Close()
	
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt)
	log.Println("Press Ctrl+C to exit")
	<-stop
	
	log.Println("Deleting commands...")
	for _, v := range registeredCommands {
		err := s.ApplicationCommandDelete(s.State.User.ID, "", v.ID)
		if err != nil {
			log.Fatalf("Cannot delete \"%v\" command: %v", v.Name, err)
		}
	}
}