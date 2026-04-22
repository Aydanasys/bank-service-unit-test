# bank-service-unit-test
# 🏦 Unit Testing — Ekip Sunumu

> **BIL-312.040101 YAZILIM MÜHENDİSLİĞİ dersi** kapsamında hazırlanmış ekip projesi.

| | |
|:---|:---|
| **Konu** | Unit Testing — PyTest |
| **Proje** | BankAccount Service |

---

## 📋 İçindekiler

0. [Ekip ve Proje Tanımı](#0-ekip-ve-proje-tanımı)
1. [Unit Test Nedir ve Neden Önemlidir?](#1-unit-test-nedir-ve-neden-önemlidir)
2. [SDLC'deki Yeri](#2-sdlcdeki-yeri)
3. [Test Senaryosu Türleri](#3-test-senaryosu-türleri)
4. [Dependency Injection](#4-dependency-injection)
5. [Mock ve Fixture](#5-mock-ve-fixture)
6. [Coverage Raporu Nedir?](#6-coverage-raporu-nedir)
7. [Test Borcu (Test Debt)](#7-test-borcu-test-debt)
8. [Workflow-Proje Süreci](#8-workflow-proje-süreci)
9. [Proje Dosyaları](#9-proje-dosyaları)

---

## 0. Ekip ve Proje Tanımı

| Rol | İsim | Sorumluluk |
|:---|:---|:---|
| Project Manager | Aydana Abdimamat kizi  | Test plan, koordinasyon |
| Backend Engineer | Salidat Cakipbekova | Kod + unit test yazımı |
| QA Engineer | Saykal Daniyar kizi | Coverage, analiz, bug tespiti |


**Proje:** BankAccount Service  

Bu projede bir banka hesabı sistemi geliştirdik ve  
unit testler ile doğruluğunu garanti altına aldık.

### Özellikler:
- Para yatırma (`deposit`)
- Para çekme (`withdraw`)
- Transfer işlemi (`transfer`)
- Hesap dondurma (`freeze_account`)
- İşlem geçmişi (`transaction_history`)

---

## 1. Unit Test Nedir ve Neden Önemlidir?

Unit test, bir fonksiyonun veya metodun **tek başına, izole** şekilde
doğru çalışıp çalışmadığını kontrol eden otomatik testtir.

> 💡 Bir araba üretirken her parçayı ayrı test etmek gibi.  
> Motor, fren ve direksiyon ayrı ayrı test edilir — böylece tüm sistem güvenli olur.

### Neden yazarız?

- Kodu değiştirdiğinde başka bir şeyi bozup bozmadığını anında anlarsın
- Hataları production'a çıkmadan önce yakalarısın
- Kod daha okunabilir ve bakımı kolay hale gelir

### Bir unit testin anatomisi — AAA Pattern:

```python
def test_deposit_increases_balance(account):
    # Arrange — test verisini hazırla
    account = BankAccount(owner="Alice", initial_balance=1000)

    # Act — fonksiyonu çalıştır
    account.deposit(500)

    # Assert — sonucu doğrula
    assert account.get_balance() == 1500
```

---

## 2. SDLC'deki Yeri

Unit test, yazılım geliştirme yaşam döngüsünün (SDLC) **geliştirme aşamasında**,
kod yazımıyla eş zamanlı uygulanır.

```
Gereksinimler  →  Tasarım  →  Geliştirme  →  Test  →  Deployment
                                    ↑
                              Unit Test burada yazılır
                              (kod yazılırken veya hemen sonrasında)
```

> Geleneksel akışta testler geliştirme sonrasına bırakılırdı.
> Modern yaklaşımda ise birim testler kodun ayrılmaz parçasıdır —
> hatta **TDD** (Test-Driven Development) yaklaşımında önce test yazılır,
> sonra kod yazılır.

---

## 3. Test Senaryosu Türleri

Her test senaryosu bir amaca hizmet eder:

| Tür | Açıklama | Örnek |
|:---|:---|:---|
| **Pozitif** | Normal, beklenen akış | 1000 bakiyeye 500 yatır → 1500 olur |
| **Negatif / Edge Case** | Hatalı veya sınır girdiler | Negatif tutar yatır → hata fırlatılmalı |
| **Boundary** | Tam sınır değerleri | Tam bakiyeyi çek → bakiye 0 olmalı |
| **Mock Doğrulama** | Davranış kontrolü | Deposit sonrası DB kayıt çağrısı yapıldı mı? |

### Edge case neden önemli?

Gerçek kullanıcılar beklenmedik şeyler yapar:
sıfır girer, negatif değer girer, dondurulmuş hesaba işlem yapmaya çalışır.
Bunları test etmezsen bu hatalar production'da ortaya çıkar.

---

## 4. Dependency Injection

Sınıfın ihtiyaç duyduğu nesneleri (database, notifier) **içeride oluşturmak**
yerine **dışarıdan parametre olarak almak** prensibidir.

### Fark nedir?

```python
# ❌ DI YOK — test edilemez
class BankAccount:
    def __init__(self):
        self.db = Database()        # içeride oluşturuluyor
        self.notifier = Notifier()  # içeride oluşturuluyor
        # Testte bu nesneleri değiştiremeyiz!
```

```python
# ✅ DI VAR — test edilebilir
class BankAccount:
    def __init__(self, db=None, notifier=None):
        self.db = db              # dışarıdan geliyor
        self.notifier = notifier  # dışarıdan geliyor
        # Testte istediğimiz nesneyi verebiliriz
```

### Neden kritik?

DI olmadan test yazmak için gerçek bir veritabanına,
gerçek bir ağ bağlantısına ihtiyaç duyarsın.
Bu testleri yavaş, kırılgan ve ortama bağımlı yapar.

DI ile testlerde **sahte (Mock) nesneler** kullanırsın —
hızlı, izole ve güvenilir.

---

## 5. Mock ve Fixture

### Mock nedir?

Gerçek bir nesnenin davranışını taklit eden sahte nesnedir.
Gerçek DB'ye bağlanmadan, `db.save()` çağrısının yapılıp yapılmadığını
kontrol edebilirsin.

```python
mock_db = MagicMock()                      # sahte veritabanı
mock_db.save.assert_called_once()          # çağrıldı mı?
mock_db.save.assert_called_once_with({..}) # doğru argümanla mı?
```

### Fixture nedir?

Birden fazla testte kullanılan **ortak test verisini** bir kez tanımlama yöntemidir.
Her test için tekrar tekrar aynı nesneyi oluşturmak yerine
pytest otomatik olarak hazırlar ve enjekte eder.

```python
@pytest.fixture
def account():
    return BankAccount(
        owner="Alice",
        initial_balance=1000,
        db=MagicMock(),
        notifier=MagicMock()
    )

# Her test bu fixture'ı otomatik alır
def test_deposit(account):
    account.deposit(500)
    assert account.get_balance() == 1500
```

---

## 6. Coverage Raporu Nedir?

Coverage (kod kapsama), testlerin kaynak kodun **yüzde kaçını çalıştırdığını** gösterir.

```bash
pytest test_bank_account.py --cov=bank_account --cov-report=term-missing
```

```
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
bank_account.py      45      9    80%   52, 53, 67-69
```

| Sütun | Anlamı |
|:---|:---|
| `Stmts` | Toplam satır sayısı |
| `Miss` | Test edilmeyen satır sayısı |
| `Cover` | Kapsama yüzdesi |
| `Missing` | Test edilmeyen satır numaraları |

> **%60 endüstriyel minimum kabul edilen eşiktir.**
> Bu projede hedef: **%80**

---

## 7. Test Borcu (Test Debt)

Test borcu, bilinçli olarak test yazılmamaya karar verilen alanlardır.
Teknik bir eksiklik değil, **bilinçli bir önceliklendirme kararıdır.**

Tıpkı finansal borç gibi: şimdi ödeme yapmazsın ama ileride mutlaka ödersin.
Ne kadar uzun ertelersen, o kadar maliyetli hale gelir.

```
Test Debt = Yazılmayan test × Zaman
```

---

## 8. Workflow Proje Süreci

Proje aşağıdaki sırayla geliştirildi:

1. Test plan oluşturuldu → [test-plan.md](./test-plan.md)
2. Sistem tasarlandı (BankAccount)
3. Dependency Injection uygulandı
4. Unit testler yazıldı
5. Mock nesneler ile bağımlılıklar izole edildi
6. Fixture yapısı ile test verileri düzenlendi
7. Testler çalıştırıldı ve doğrulandı
8. Coverage analizi yapıldı → [QA_Kapsam_Raporu_v2.docx](./QA_Kapsam_Raporu_v2.docx)
9. Test edilmemiş alanlar test debt olarak belirlendi
10. Pull Request süreci tamamlandı

---

## 9. Proje Dosyaları

| Dosya | Açıklama |
|:---|:---|
| [`bank_account.py`](./bank_account.py) | BankAccount sınıfı — Dependency Injection uygulandı |
| [`database.py`](./database.py) | Gerçek DB sınıfı |
| [`notifier.py`](./notifier.py) | Gerçek Notifier sınıfı |
| [`test_bank_account.py`](./test_bank_account.py) | 15 unit test |
| [`test-plan.md`](./test-plan.md) | Test planı — kod öncesi hazırlandı |
| [`QA_Kapsam_Raporu_v2.docx`](./QA_Kapsam_Raporu_v2.docx) | Coverage raporu ve bug listesi |
| [`requirements.txt`](./requirements.txt) | Proje bağımlılıkları |
