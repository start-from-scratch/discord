package main 

import (
	"os"
	"log"
	"os/signal"
	"net/http"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	cfg, err := LoadConfig("./config.json")
	if err != nil {
		log.Fatal(err)
	}

	s, err := StartBot(cfg)
	if err != nil {
		log.Fatal(err)
	}
	defer StopBot(s)

  go func() {
		http.Handle("/metrics", promhttp.Handler())
		http.ListenAndServe(cfg.Metrics.Port, nil)
	}()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt)
	log.Println("Press Ctrl+C to exit")
	<-stop
}