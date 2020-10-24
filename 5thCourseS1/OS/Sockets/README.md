# Sockets implementation on C with INET and UNIX domains.


## Benchmarks tested on WSL

### Socket creation time
|  | Blocking | Nonblocking |
|---------------|----------|-------------|
| INET          | 55 us    | 68 us       |
| UNIX          | 34 us    | 31 us       |

### Socket closing time
|  | Blocking | Nonblocking |
|--------------|----------|-------------|
| INET         | 29 us    | 27 us       |
| UNIX         | 10.5 us  | 107.75 us   |

### Socket data transferring time for 1Gb with packet size 1Kb
|  | Blocking           | Nonblocking        |
|------------------|--------------------|--------------------|
| INET             | 16.6 s  | 18.6 s  |
| UNIX             | 6 s    | 13 s    |

### Socket data transferring speed for 1Gb with packet size 1Kb
|  | Blocking           | Nonblocking        |
|------------------|--------------------|--------------------|
| INET             |  60.2 Mb/s |  53.8 Mb/s |
| UNIX             |  166.7 Mb/s   |  76.9 Mb/s   |