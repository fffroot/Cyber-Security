CC = gcc
CFLAGS = -Wall -Wextra -pthread
TARGET = scanner

all: $(TARGET)

$(TARGET): port_scanner.c
	$(CC) $(CFLAGS) -o $(TARGET) port_sc Broadcaster.c

clean:
	rm -f $(TARGET)

.PHONY: all clean