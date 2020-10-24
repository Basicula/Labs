#include "Common.h"

int run_server(enum FamilyType family_type, enum ConnectionMode connection_mode)
{
  int server, connection;
  char hello_message[] = "Hello from server";
  char packet[PACKET_SIZE];
  struct sockaddr_in addr_in;
  struct sockaddr_un addr_un;
  struct sockaddr* addr;
  int family;
  int addr_len;
  double start_time, now;

  switch (family_type)
  {
  case INET:
    family = AF_INET;
    addr_in.sin_family = family;
    addr_in.sin_addr.s_addr = INADDR_ANY;
    addr_in.sin_port = htons(PORT);
    addr = (struct sockaddr*)&addr_in;
    addr_len = sizeof(addr_in);
    break;
  case UNIX:
    family = AF_UNIX;
    addr_un.sun_family = family;
    strcpy(addr_un.sun_path, SOCKET_FILE);
    unlink(SOCKET_FILE);
    addr = (struct sockaddr*)&addr_un;
    addr_len = sizeof(addr_un.sun_family) + strlen(addr_un.sun_path);
    break;
  default:
    printf("Undefined family type for server");
    return -1;
  }

  printf("Creating socket...");
  start_time = get_time();
  if ((server = socket(family, SOCK_STREAM, 0)) < 0)
  {
    printf("Could not create socket");
    return -1;
  }
  now = get_time();
  printf("Socket created in %.06f us\n", now - start_time);

  if (apply_connection_mode(&server, connection_mode) < 0)
  {
    printf("Applying connection mode failed\n");
    return -1;
  }

  printf("Binding socket...");
  start_time = get_time();
  if (bind(server, addr, addr_len) < 0)
  {
    printf("Bind failed\n");
    return -1;
  }
  now = get_time();
  printf("Bind done in %.06f us\n", now - start_time);

  if (listen(server, 10) < 0)
  {
    printf("Listen failed");
    return -1;
  }

  printf("Waiting for incoming connections...\n");

  while (1)
  {
    connection = accept(server, NULL, NULL);
    
    if (connection < 0)
    {
      if (connection_mode == BLOCKING)
      {
        printf("Accept connection failed\n");
        return -1;
      }
      else
      {
        sleep(1);
        continue;
      }
    }
    printf("Connection accepted\n");
    
    int pid = fork();
    if (pid < 0) {
      printf("ERROR on fork");
      return -1;
    }

    if (pid == 0)
    {
      int packet_cnt = 0;
      int cnt;
      start_time = get_time();
      while ((cnt = read(connection, packet, PACKET_SIZE)) > 0)
        ++packet_cnt;
      now = get_time();
      printf("Accepted %d packets with packet size %d read in %.06f s\n", packet_cnt, PACKET_SIZE, (now - start_time) / 1000000);

      start_time = get_time();
      close(connection);
      now = get_time();
      printf("Connection closed in %.06f us\n", now - start_time);
    }
    else
      close(connection);
  }

  start_time = get_time();
  close(server);
  now = get_time();
  printf("Server closed in %.06f\n", now - start_time);

  return 0;
}

int main(int argc, char* argv[])
{
  if (run_server(UNIX, BLOCKING) < 0)
  {
    printf("Failed to run server\n");
    return 1;
  }
  return 0;
}