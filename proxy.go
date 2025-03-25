package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"strings"
)

// Configuration
const (
	proxyPort      = 8545
	targetHost     = "localhost:7788"
	targetProtocol = "http"
)

func main() {
	// Create target URL
	targetURL, err := url.Parse(fmt.Sprintf("%s://%s", targetProtocol, targetHost))
	if err != nil {
		log.Fatalf("Failed to parse target URL: %v", err)
	}

	// Handler for all incoming requests
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Log incoming request
		log.Printf("Received request: %s %s", r.Method, r.URL.Path)

		// Create a new URL from the raw RequestURI sent by the client
		url := *r.URL
		url.Host = targetHost
		url.Scheme = targetProtocol

		// Create the proxy request
		proxyReq, err := http.NewRequest(r.Method, url.String(), r.Body)
		if err != nil {
			http.Error(w, fmt.Sprintf("Error creating proxy request: %v", err), http.StatusInternalServerError)
			return
		}

		// Copy the headers from original request
		for name, values := range r.Header {
			// Skip the Connection header to avoid problems with persistent connections
			if strings.ToLower(name) == "connection" {
				continue
			}
			for _, value := range values {
				proxyReq.Header.Add(name, value)
			}
		}

		// Update the Host header to match the target
		proxyReq.Host = targetHost

		// Send the request to the target server
		client := &http.Client{}
		resp, err := client.Do(proxyReq)
		if err != nil {
			http.Error(w, fmt.Sprintf("Error forwarding request to target: %v", err), http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()

		// Copy response headers from target to client
		for name, values := range resp.Header {
			for _, value := range values {
				w.Header().Add(name, value)
			}
		}

		// Copy status code
		w.WriteHeader(resp.StatusCode)

		// Copy the response body from target to client
		_, err = io.Copy(w, resp.Body)
		if err != nil {
			log.Printf("Error copying response body: %v", err)
			return
		}

		log.Printf("Successfully proxied request: %s %s", r.Method, r.URL.Path)
	})

	// Start the server
	listenAddr := fmt.Sprintf("0.0.0.0:%d", proxyPort)
	log.Printf("Starting proxy server on %s, forwarding to %s", listenAddr, targetURL)
	err = http.ListenAndServe(listenAddr, nil)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
