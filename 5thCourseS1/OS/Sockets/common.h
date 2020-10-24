#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <time.h>

#define PORT 8080
#define INET_ADDR "192.168.0.100"
#define PACKET_SIZE 1024
#define NUM_OF_PACKETS 1024 * 1024

enum FamilyType
{
  INET,
  UNIX
};

enum ConnectionMode
{
  BLOCKING,
  NONBLOCKING
};

int apply_connection_mode(int* socket, enum ConnectionMode connection_mode);
double get_time();

#endif // COMMON_H