# Smart-Lab-IoT-Project

# 🌡️ Smart Lab Environmental Monitoring System

Sistem IoT *End-to-End* untuk memantau suhu ruang server/laboratorium secara *real-time* dengan integrasi Kecerdasan Buatan (AI) untuk deteksi dini anomali suhu (*Overheat/Freeze*).

## 🚀 Fitur Utama
* **Real-time Monitoring:** Visualisasi data suhu menggunakan Grafik Interaktif (Chart.js).
* **AI Integration:** Deteksi status keamanan (Normal/Warning/Critical) menggunakan algoritma *Rule-Based System*.
* **Analog Precision:** Menggunakan sensor LM35 dengan kalibrasi ADC untuk akurasi tinggi.
* **Cloud Architecture:** Backend berbasis Python (Flask) yang di-hosting di PythonAnywhere.

## 🛠️ Arsitektur Sistem
Sistem ini terdiri dari dua lapisan utama:
1.  **Edge Device (Hardware):** ESP32 + Sensor LM35.
2.  **Cloud Platform (Software):** Python Flask + HTML5 Dashboard.
