# Build stage
FROM golang:1.24-alpine AS builder
WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN go build -o genx_bridge main.go

# Run stage
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/genx_bridge .
EXPOSE 8080
CMD ["./genx_bridge"]
