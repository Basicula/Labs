#include "Common.h"

#include <arpa/inet.h>

void fill_buff(char buff[PACKET_SIZE])
{
  for (int i = 0; i < PACKET_SIZE; ++i)
    buff[i] = i;
}

int run_client(enum FamilyType family_type, enum ConnectionMode connection_mode)
{
  int client, n;
  char buff[PACKET_SIZE];
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
    addr_in.sin_port = htons(PORT);
    addr = (struct sockaddr*)&addr_in;
    addr_len = sizeof(addr_in);
    if (inet_pton(family, INET_ADDR, &addr_in.sin_addr) <= 0)
    {
      printf("\n inet_pton error occured\n");
      return 1;
    }
    break;
  case UNIX:
    family = AF_UNIX;
    addr_un.sun_family = family;
    strcpy(addr_un.sun_path, SOCKET_FILE);
    addr = (struct sockaddr*)&addr_un;
    addr_len = sizeof(addr_un.sun_family) + strlen(addr_un.sun_path);
    break;
  default:
    printf("Undefined family type for server");
    return -1;
  }

  if ((client = socket(family, SOCK_STREAM, 0)) < 0)
  {
    printf("\n Error : Could not create socket \n");
    return 1;
  }

  if (connect(client, addr, addr_len) < 0)
  {
    printf("\n Error : Connect Failed \n");
    return 1;
  }

  fill_buff(buff);

  start_time = get_time();
  for (int i = 0; i < NUM_OF_PACKETS; ++i)
  {
    write(client, buff, PACKET_SIZE);
  }
  now = get_time();
  printf("1gb info sent in %.06f s\n", (now - start_time) / 1000000);

  if (n < 0)
  {
    printf("\n Read error \n");
  }
}

int main(int argc, char* argv[]) {
  
  if (run_client(UNIX, BLOCKING) < 0)
  {
    printf("Failed to run client\n");
    return 1;
  }
  return 0;
}