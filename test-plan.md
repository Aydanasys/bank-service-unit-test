# 🏦 BankAccount Service — Software Test Plan (STP)

Bu doküman, bank-service-unit-test projesinin test stratejisini ve kabul
kriterlerini tanımlar. Kod yazımına başlanmadan önce hazırlanmıştır.

Hazırlayan: [PM İsmi]  
Rol: Project Manager  
Tarih: 22.04.2026  
Durum: Taslak (İncelemeye Hazır)

---

## 1. Test Amacı ve Kapsamı

Bu projenin amacı, BankAccount sınıfının finansal iş mantığını
(para yatırma, çekme, transfer) birim testlerle doğrulamak ve
sistemin hatalı girdilere karşı dayanıklılığını ölçmektir.

- Test Seviyesi: Birim Test (Unit Testing)
- Test Nesnesi: BankAccount sınıfı ve public metodları
- Test Araçları: PyTest, pytest-cov, unittest.mock.MagicMock
- Kapsam Dışı: UI testleri, gerçek veritabanı entegrasyonu, performans testleri

---

## 2. Proje Dosya Yapısı

Geliştirme ekibinin oluşturması beklenen dosyalar:
<img width="766" height="281" alt="image" src="https://github.com/user-attachments/assets/629bf8c8-641e-4bda-8477-086af04eca82" />


## 3. Modül Test Önceliklendirme Matrisi

Test faaliyetleri, iş riskine ve finansal etkiye göre
aşağıdaki hiyerarşi ile yürütülecektir:

| Öncelik | Metot | Risk Seviyesi | Test Odağı |
| :--- | :--- | :--- | :--- |
| P0 (Kritik) | transfer() | Çok Yüksek | Hesaplar arası bakiye tutarlılığı ve atomik işlem doğruluğu |
| P0 (Kritik) | withdraw() | Yüksek | Yetersiz bakiye ve negatif tutar kontrolleri |
| P1 (Yüksek) | deposit() | Orta | Pozitif bakiye artışı, DB ve Notifier tetikleyici kontrolü |
| P1 (Yüksek) | freeze_account() | Orta | Dondurulmuş hesaplarda işlem kısıtlamalarının aktifliği |
| P2 (Orta) | get_balance() | Düşük | Doğru bakiye dönüşü |
| P3 (Düşük) | transaction_history() | Düşük | İşlem geçmişi verilerinin doğru dönmesi |

---

## 4. Test Metodolojisi ve İzolasyon Stratejisi

### Dependency Injection Yaklaşımı

BankAccount sınıfı, Database ve Notifier bağımlılıklarını
dışarıdan alacak şekilde tasarlanacaktır. Bu sayede testlerde
gerçek nesneler yerine MagicMock enjekte edilebilecektir.
<img width="842" height="267" alt="image" src="https://github.com/user-attachments/assets/1297efc6-1042-43db-8c03-4f03dfabd8e1" />

### Kullanılacak Teknikler

- Boundary Value Analysis: Sınır değer testleri
  (0, negatif değer, tam bakiyeye eşit tutar)
- Error Guessing: Olası hata senaryoları
  (dondurulmuş hesap, negatif başlangıç bakiyesi)
- Mock Doğrulama: assert_called_once() ile
  DB ve Notifier çağrılarının kontrolü

---

## 5. Planlanacak Test Senaryoları

### deposit() — 5 test planlandı
| # | Senaryo | Tür | Beklenen Sonuç |
|---|---|---|---|
| 1 | Normal para yatırma | Pozitif | Bakiye artar |
| 2 | DB save çağrısı kontrolü | Mock | db.save 1 kez çağrılmalı |
| 3 | Notifier çağrısı kontrolü | Mock | notifier.notify 1 kez çağrılmalı |
| 4 | Negatif tutar | Edge Case | ValueError fırlatılmalı |
| 5 | Sıfır tutar | Edge Case | ValueError fırlatılmalı |

### withdraw() — 4 test planlandı
| # | Senaryo | Tür | Beklenen Sonuç |
|---|---|---|---|
| 6 | Normal para çekme | Pozitif | Bakiye azalır |
| 7 | Bakiyeden fazla çekme | Edge Case | ValueError fırlatılmalı |
| 8 | Sıfır tutar | Edge Case | ValueError fırlatılmalı |
| 9 | Tam bakiyeyi çekme | Boundary | Bakiye 0 olmalı |

### transfer() — 3 test planlandı
| # | Senaryo | Tür | Beklenen Sonuç |
|---|---|---|---|
| 10 | Normal transfer | Pozitif | Her iki bakiye güncellenmeli |
| 11 | Yetersiz bakiyeyle transfer | Edge Case | ValueError fırlatılmalı |
| 12 | Negatif tutarlı transfer | Edge Case | ValueError fırlatılmalı |

### freeze_account() — 2 test planlandı
| # | Senaryo | Tür | Beklenen Sonuç |
|---|---|---|---|
| 13 | Dondurulmuş hesaba deposit | Edge Case | PermissionError fırlatılmalı |
| 14 | Dondurulmuş hesaptan withdraw | Edge Case | PermissionError fırlatılmalı |

### init() — 1 test planlandı
| # | Senaryo | Tür | Beklenen Sonuç |
|---|---|---|---|
| 15 | Negatif başlangıç bakiyesi | Edge Case | ValueError fırlatılmalı |

## 6. Kabul ve Çıkış Kriterleri (Exit Criteria)

Projenin tamamlanmış sayılabilmesi için aşağıdaki şartların
sağlanması gerekmektedir:

1. P0 ve P1 öncelikli tüm testler hatasız (Passed) tamamlanmalıdır
2. Kod kapsama oranı (coverage) minimum %60 olmalıdır
3. Hiçbir açık P0 veya P1 seviyesinde bug bulunmamalıdır

---

## 7. Planlanan Test Borcu (Planned Test Debt)

Aşağıdaki alanlar bu sprint kapsamı dışında tutulmuş,
ileriki sprintlere planlanmıştır:

| Kapsam Dışı Alan | Gerekçe | Risk |
|---|---|---|
| transaction_history() | Düşük öncelik, sprint kapasitesi sınırlı | Düşük |
| Race Conditions | Asenkron test altyapısı henüz hazır değil | Orta |
| DB bağlantı kopması | Resiliency test ortamı kurulmadı | Orta |

---

## 8. Haftalık Rapor Şablonu

> Bu bölüm testler tamamlandıktan sonra QA tarafından doldurulacaktır.

| Hafta | Toplam Test | Passed | Failed | Coverage |
|---|---|---|---|---|
| Sprint 1 | 15 | 15 | 0 | 93 |

---


## 9. Sorumluluklar

| Rol | Sorumluluk |
|---|---|
| Project Manager | Test planı hazırlama, önceliklendirme, haftalık rapor takibi |
| Backend Engineer | DI uygulaması, test yazımı, PR açma |
| QA | Coverage raporu, bug listesi, mock/fixture doğrulama, PR onayı |
