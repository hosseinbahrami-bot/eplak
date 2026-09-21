/* portfix.c — environment-level shim (NOT part of the app).
   The app's shared/bootstrap.php passes a URL ('https://eplak.ir/') where a
   MySQL hostname is expected, so mysqlnd parses the port as 0. This shim
   rewrites TCP connects to port 0 into port 3306 (local MariaDB), letting the
   project run unmodified. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

typedef int (*connect_t)(int, const struct sockaddr *, socklen_t);

int connect(int fd, const struct sockaddr *addr, socklen_t len) {
    static connect_t real = NULL;
    if (!real) real = (connect_t)dlsym(RTLD_NEXT, "connect");

    if (addr && addr->sa_family == AF_INET) {
        struct sockaddr_in *s = (struct sockaddr_in *)addr;
        if (ntohs(s->sin_port) == 0) {
            struct sockaddr_in c;
            memcpy(&c, s, sizeof(c));
            c.sin_port = htons(3306);
            return real(fd, (const struct sockaddr *)&c, len);
        }
    } else if (addr && addr->sa_family == AF_INET6) {
        struct sockaddr_in6 *s = (struct sockaddr_in6 *)addr;
        if (ntohs(s->sin6_port) == 0) {
            struct sockaddr_in6 c;
            memcpy(&c, s, sizeof(c));
            c.sin6_port = htons(3306);
            return real(fd, (const struct sockaddr *)&c, len);
        }
    }
    return real(fd, addr, len);
}
