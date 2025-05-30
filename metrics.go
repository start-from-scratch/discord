package main

import (
  "time"

  "github.com/bwmarrin/discordgo"
  "github.com/prometheus/client_golang/prometheus"
)

var (
  commandsUsed = prometheus.NewCounterVec(
    prometheus.CounterOpts{
      Name: "discord_commands_total",
      Help: "Total number of commands used",
    },
    []string{"command"},
  )

  latencyGauge = prometheus.NewGauge(
    prometheus.GaugeOpts{
      Name: "discord_bot_latency_ms",
      Help: "Current Discord gateway latency in milliseconds",
    },
  )
)

func init() {
	prometheus.MustRegister(commandsUsed, latencyGauge)
}

func StartTracker(s *discordgo.Session, cfg Config) {
  ticker := time.NewTicker(cfg.Metrics.Delay)

  go func() {
    for range ticker.C {
      latency := s.HeartbeatLatency().Milliseconds()
      latencyGauge.Set(float64(latency))
    }
  }()
}