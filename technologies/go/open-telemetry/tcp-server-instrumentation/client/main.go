package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"

	"go.opentelemetry.io/otel/api/global"
	"go.opentelemetry.io/otel/api/trace"
	"go.opentelemetry.io/otel/label"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
)

func processTCPRequest(tracer trace.Tracer, listener net.Listener) {
	// Accept TCP request
	conn, _ := listener.Accept()
	defer conn.Close()
	conn.Write([]byte("Hello from TCP server"))

	// Create custom Span that represent accepted TCP connection
	_, connSpan := tracer.Start(context.Background(), "Incoming TCP connection")
	defer connSpan.End()

	// Set client IP address as Span attribute
	connSpan.SetAttributes(label.KeyValue{
		Key:   "Client address",
		Value: label.StringValue(conn.LocalAddr().String()),
	})

	// Do HTTP request
	resp, _ := http.Get("http://127.0.0.1:8080/")
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
}

func main() {
	// Init SDK Tracer
	global.SetTracerProvider(sdktrace.NewTracerProvider())
	tracer := global.Tracer("TracerName")

	// Start TCP server
	listener, _ := net.Listen("tcp", ":1234")
	for {
		processTCPRequest(tracer, listener)
	}
}
