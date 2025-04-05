# ARP Detection Script

Skrip ini ditulis menggunakan bahasa Python dan dirancang untuk mendeteksi anomali dalam jaringan, khususnya aktivitas *excessive ARP requests*. Skrip dijalankan di perangkat berbasis Linux seperti Raspberry Pi, dan menggunakan beberapa library Python seperti `subprocess`, `asyncio`, dan `re`.

Dengan menjalankan perintah `tcpdump`, skrip memantau lalu lintas ARP secara *asynchronous* dan menerapkan pola *regex* untuk mendeteksi permintaan ARP yang berlebihan dari alamat IP tertentu. Jika jumlah permintaan ARP dari suatu IP melebihi ambang batas dalam jangka waktu tertentu, skrip akan menganggapnya sebagai potensi serangan.

Anomali ini kemudian dikirimkan secara *real-time* ke saluran Discord menggunakan bot yang terhubung melalui API Discord. Mekanisme pembatasan jumlah pesan juga diterapkan untuk mencegah spam.

Dengan cara ini, administrator jaringan dapat menerima notifikasi secara langsung ketika terdeteksi aktivitas mencurigakan di jaringan mereka.

---
Contoh Topologi: 

![Diagram ARP Detection](topology_example.jpg)

---
## Catatan
- Pastikan perangkat berada dalam satu jaringan yang sama.
- Lakukan uji coba dengan Nmap atau tools sejenisnya untuk scan jaringan.