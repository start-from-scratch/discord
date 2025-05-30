FROM golang:1.24.1 AS build
WORKDIR /bot/
COPY go.mod go.sum ./
RUN go mod download
COPY ./ ./
RUN go build -o bot .

FROM scratch
COPY --from=builder /bot/bot /bot/config.json /bot/
VOLUME [ "/bot/config.json" ]
ENTRYPOINT [ "/bot/bot" ]