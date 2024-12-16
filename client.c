#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>  // Windows TCP/IP başlık dosyası
#pragma comment(lib, "ws2_32.lib")  // Winsock kütüphanesini bağlama

int main() {
    WSADATA wsa;  // Windows için WSA veri yapısı
    SOCKET sock;  // Windows soket türü
    struct sockaddr_in server_address;
    char student_id[10];
    char server_response[1024];

    // 1. Winsock kütüphanesini başlat
    printf("Winsock başlatılıyor...\n");
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        printf("WSAStartup hatası: %d\n", WSAGetLastError());
        return 1;
    }

    // 2. Soket oluştur
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        printf("Soket oluşturma hatası: %d\n", WSAGetLastError());
        return 1;
    }

    // 3. Server ayarları
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(12345);  // Server portu
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");  // Server IP adresi

    // 4. Server'a bağlan
    if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        printf("Bağlantı hatası.\n");
        return 1;
    }

    printf("Server'a bağlanıldı.\n");

    // 5. Kullanıcıdan öğrenci numarasını al
    printf("Öğrenci numarasını girin: ");
    scanf("%s", student_id);

    // 6. Server'a öğrenci numarasını gönder
    send(sock, student_id, strlen(student_id), 0);

    // 7. Server'dan gelen cevabı al
    int recv_size = recv(sock, server_response, sizeof(server_response), 0);
    if (recv_size > 0) {
        server_response[recv_size] = '\0';  // Gelen string'i sonlandır
        printf("Server'dan gelen cevap: %s\n", server_response);
    } else {
        printf("Server'dan veri alınamadı.\n");
    }

    // 8. Soketi kapat
    closesocket(sock);
    WSACleanup();  // Winsock'u kapat

    return 0;
}
