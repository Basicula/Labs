#include "Common.h"

#include <fcntl.h>

double get_time()
{
  struct timespec tms;
  clock_gettime(CLOCK_REALTIME, &tms);
  return tms.tv_sec * 1000000.0 + tms.tv_nsec / 1000.0;
}

int apply_connection_mode(int* socket, enum ConnectionMode connection_mode)
{
  int flags = fcntl(*socket, F_GETFL, 0);
  if (flags == -1)
    return -1;
  switch (connection_mode)
  {
  case BLOCKING:
    flags &= ~O_NONBLOCK;
    if (fcntl(*socket, F_SETFL, flags) != 0)
    {
      printf("Failed to set fcntl flags\n");
      return -1;
    }
    break;
  case NONBLOCKING:
    flags |= O_NONBLOCK;
    if (fcntl(*socket, F_SETFL, flags) != 0)
    {
      printf("Failed to set fcntl flags\n");
      return -1;
    }
    break;
  default:
    printf("Undefined connection block\n");
    return -1;
  }
  return 0;
}

int configure_socket(int* ip_socket, enum FamilyType family_type, enum ConnectionMode connection_mode)
{
  struct sockaddr_in addr_in;
  struct sockaddr_un addr_un;
  struct sockaddr* addr;
  int family;
  int addr_len, opt = 1;
  socklen_t socklen_addr_in = sizeof(addr_in);

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
  if ((*ip_socket = socket(family, SOCK_STREAM, 0)) < 0)
  {
    printf("Could not create socket");
    return -1;
  }
  printf("Socket created.\n");

  if (apply_connection_mode(ip_socket, connection_mode) < 0)
  {
    printf("Applying connection mode failed\n");
    return -1;
  }

  printf("Binding socket...");
  if (bind(*ip_socket, addr, addr_len) < 0)
  {
    printf("Bind failed\n");
    return -1;
  }
  printf("Bind done\n");
}