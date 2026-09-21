/* bindfix.c — environment-level shim (NOT part of the app).
   backend/server.js hardcodes port 8080, already used by the PHP site here.
   This shim remaps that bind to 3000 so the Node backend runs unmodified. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

typedef int (*bind_t)(int, const struct sockaddr *, socklen_t);

int bind(int fd, const struct sockaddr *addr, socklen_t len) {
    static bind_t real = NULL;
    if (!real) real = (bind_t)dlsym(RTLD_NEXT, "bind");

    if (addr && addr->sa_family == AF_INET) {
        struct sockaddr_in *s = (struct sockaddr_in *)addr;
        if (ntohs(s->sin_port) == 8080) {
            struct sockaddr_in c;
            memcpy(&c, s, sizeof(c));
            c.sin_port = htons(3000);
            return real(fd, (const struct sockaddr *)&c, len);
        }
    } else if (addr && addr->sa_family == AF_INET6) {
        struct sockaddr_in6 *s = (struct sockaddr_in6 *)addr;
        if (ntohs(s->sin6_port) == 8080) {
            struct sockaddr_in6 c;
            memcpy(&c, s, sizeof(c));
            c.sin6_port = htons(3000);
            return real(fd, (const struct sockaddr *)&c, len);
        }
    }
    return real(fd, addr, len);
}
