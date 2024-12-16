import sqlite3
import socket

# 1. Veritabanı Oluşturma (Aynı kod)
# Veritabanı bağlantısı
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Eğer tablo zaten varsa sil
cursor.execute('DROP TABLE IF EXISTS Grades')

# Tabloyu yeniden oluştur
cursor.execute('''
CREATE TABLE Grades (
    StudentID INTEGER PRIMARY KEY,
    Grade INTEGER
)
''')

# Veri ekleme
cursor.executemany('''
INSERT INTO Grades (StudentID, Grade) VALUES (?, ?)
''', [(1001, 85), (1002, 90), (1003, 78)])

conn.commit()
conn.close()

print("Veritabanı başarıyla temizlendi ve veriler eklendi.")


# 2. TCP Server Kısmı
# Veritabanından notları alacak fonksiyon
def get_grade(student_id):
    conn = sqlite3.connect('students.db')  # Veritabanı bağlantısı
    cursor = conn.cursor()
    cursor.execute("SELECT Grade FROM Grades WHERE StudentID = ?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Server kurulumu
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # IP adresi ve port numarası
server_socket.listen(5)  # Maksimum 5 bağlantı kuyruğu
print("Server dinlemede...")

# Client bağlantılarını dinle
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Bağlantı kabul edildi: {client_address}")

    # İstemciden öğrenci numarasını al
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Gelen öğrenci numarası: {data}")

    # Veritabanından notu sorgula
    try:
        student_id = int(data)  # Gelen veriyi tam sayıya dönüştür
        grade = get_grade(student_id)
        response = str(grade) if grade else "Not bulunamadı"
    except ValueError:
        response = "Geçersiz öğrenci numarası!"

    # Cevabı istemciye gönder
    client_socket.send(response.encode('utf-8'))
    print(f"Gönderilen cevap: {response}")

    # Bağlantıyı kapat
    client_socket.close()
