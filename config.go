package main

import (
	"encoding/json"
	"errors"
	"os"
	"time"
)

type BotConfig struct {
	Token string `json:"token"`
}

type MetricsConfig struct {
	Delay time.Duration `json:"delay"`
	Port  string        `json:"port"`
}

type Config struct {
	Bot     BotConfig     `json:"bot"`
	Metrics MetricsConfig `json:"metrics"`
}

func validateConfig(cfg *Config) (err error) {
	if cfg.Bot.Token == "" {
		err = errors.New("missing required config value: bot.token")
		return
	}
	cfg.Bot.Token = "Bot " + cfg.Bot.Token

	if cfg.Metrics.Delay == 0 {
		err = errors.New("missing required config value: metrics.delay")
		return
	}
	cfg.Metrics.Delay = cfg.Metrics.Delay * time.Millisecond

	if cfg.Metrics.Port == "" {
		err = errors.New("missing required config value: metrics.port")
		return
	}
	cfg.Metrics.Port = ":" + cfg.Metrics.Port

  return
}

func LoadConfig(path string) (cfg Config, err error) {
	var raw []byte

	raw, err = os.ReadFile("config.json")
  if err != nil {
    return
  }

  err = json.Unmarshal(raw, &cfg)
	if err != nil {
    return
  }

	err = validateConfig(&cfg)
	return
}