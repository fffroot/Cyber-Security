#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/select.h>
#include <pthread.h>
#include <semaphore.h>

#define TIMEOUT_MS 500
#define MAX_CONCURRENT_THREADS 500 // Ограничение одновременных потоков

sem_t thread_sem; // Семафор для контроля количества потоков

// Прототип функции
int scan_port(const char *target_ip, int port, char *banner);

// Структура аргументов для потока
typedef struct {
    const char *ip;
    int port;
} scan_args_t;

// Функция потока
void* scan_thread(void* arg) {
    scan_args_t *args = (scan_args_t *)arg;
    char banner[256] = {0};

    // Сканируем порт и пытаемся получить баннер
    int result = scan_port(args->ip, args->port, banner);

    if (result == 1) {
        if (strlen(banner) > 0) {
            printf("✅ Порт %5d: ОТКРЫТ  | Сервис: %s\n", args->port, banner);
        } else {
            printf("✅ Порт %5d: ОТКРЫТ  | Сервис: Неизвестен (нет баннера)\n", args->port);
        }
    }

    free(args);
    sem_post(&thread_sem); // Освобождаем слот в пуле потоков
    return NULL;
}

// Функция сканирования одного порта с попыткой чтения баннера
int scan_port(const char *target_ip, int port, char *banner) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return -1;

    struct sockaddr_in target;
    struct timeval tv;

    // Таймаут на подключение
    tv.tv_sec = 0;
    tv.tv_usec = TIMEOUT_MS * 1000;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));

    memset(&target, 0, sizeof(target));
    target.sin_family = AF_INET;
    target.sin_port = htons(port);
    inet_pton(AF_INET, target_ip, &target.sin_addr);

    int res = connect(sock, (struct sockaddr *)&target, sizeof(target));
    int result = 0;

    if (res == 0) {
        result = 1; // Порт открыт!

        // === BANNER GRABBING ===
        fd_set read_fds;
        struct timeval tv_banner;
        tv_banner.tv_sec = 1;  // Ждём баннер 1 секунду
        tv_banner.tv_usec = 0;

        FD_ZERO(&read_fds);
        FD_SET(sock, &read_fds);

        // Проверяем, есть ли данные для чтения
        if (select(sock + 1, &read_fds, NULL, NULL, &tv_banner) > 0) {
            int bytes = recv(sock, banner, 255, 0);
            if (bytes > 0) {
                banner[bytes] = '\0'; // Завершающий нуль

                // Очищаем баннер от переносов строк для красивого вывода
                char *p;
                if ((p = strchr(banner, '\r')) != NULL) *p = '\0';
                if ((p = strchr(banner, '\n')) != NULL) *p = '\0';
            }
        }
    }

    close(sock);
    return result;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("Использование: %s <IP> <START_PORT> <END_PORT>\n", argv[0]);
        return 1;
    }

    const char *ip = argv[1];
    int start_port = atoi(argv[2]);
    int end_port = atoi(argv[3]);

    if (start_port > end_port || start_port < 1 || end_port > 65535) {
        printf("❌ Неверный диапазон портов\n");
        return 1;
    }

    // Инициализация семафора (0 = разделяется между потоками одного процесса, MAX_CONCURRENT_THREADS = начальный счетчик)
    sem_init(&thread_sem, 0, MAX_CONCURRENT_THREADS);

    printf("🔍 Сканирую %s (порты %d-%d)\n", ip, start_port, end_port);
    printf("⚙️ Макс. потоков: %d\n\n", MAX_CONCURRENT_THREADS);

    int total_ports = end_port - start_port + 1;
    pthread_t *threads = malloc(total_ports * sizeof(pthread_t));
    int thread_count = 0;

    for (int port = start_port; port <= end_port; port++) {
        // Ждём, пока не освободится слот для нового потока
        sem_wait(&thread_sem);

        scan_args_t *args = malloc(sizeof(scan_args_t));
        args->ip = ip;
        args->port = port;

        if (pthread_create(&threads[thread_count], NULL, scan_thread, args) != 0) {
            perror("pthread_create failed");
            free(args);
            sem_post(&thread_sem); // Возвращаем слот, если создание не удалось
            continue;
        }
        thread_count++;
    }

    // Ждём завершения всех созданных потоков
    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);
    sem_destroy(&thread_sem); // Уничтожаем семафор

    printf("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("📊 Сканирование завершено.\n");

    return 0;
}