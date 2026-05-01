package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
)

type TradeData struct {
	Symbol    string  `json:"symbol"`
	Bid       float64 `json:"bid"`
	Ask       float64 `json:"ask"`
	LotSize   float64 `json:"lot_size"`
	TP        float64 `json:"tp"`
	SL        float64 `json:"sl"`
	Timestamp int64   `json:"timestamp"`
}

func validateAuth(r *http.Request) bool {
	julesKey := os.Getenv("JULES_API_KEY_V4")
	githubToken := os.Getenv("GITHUB_TOKEN_PUSH")

	authHeader := r.Header.Get("Authorization")
	expectedAuth := "Bearer " + julesKey
	if julesKey == "" || authHeader != expectedAuth {
		return false
	}

	githubHeader := r.Header.Get("X-GitHub-Token")
	if githubToken == "" || githubHeader != githubToken {
		return false
	}

	return true
}

func tradeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	if !validateAuth(r) {
		log.Printf("Unauthorized access attempt from %s", r.RemoteAddr)
		http.Error(w, `{"status":"error","message":"Unauthorized"}`, http.StatusUnauthorized)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Read error", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	var data TradeData
	if err := json.Unmarshal(body, &data); err != nil {
		log.Printf("Invalid JSON from %s: %v", r.RemoteAddr, err)
		http.Error(w, `{"status":"error","message":"Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	log.Printf("Processed trade: %+v from %s", data, r.RemoteAddr)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":   "success",
		"received": data,
	})
}

func main() {
	port := os.Getenv("BRIDGE_PORT")
	if port == "" {
		port = "8000"
	}

	julesKey := os.Getenv("JULES_API_KEY_V4")
	githubToken := os.Getenv("GITHUB_TOKEN_PUSH")

	if julesKey == "" || githubToken == "" {
		log.Fatal("JULES_API_KEY_V4 and GITHUB_TOKEN_PUSH must be set")
	}

	http.HandleFunc("/", tradeHandler)

	log.Printf("GenX Go Bridge starting on port %s...", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}
