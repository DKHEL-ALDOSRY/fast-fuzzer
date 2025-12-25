# 🚀 Fast-Fuzzer

**Fast-Fuzzer** هي أداة متطورة وعالية الأداء مخصصة لخبراء الأمن السيبراني، مصممة لفحص المسارات (Directories) والنطاقات الفرعية (Subdomains) بسرعة فائقة باستخدام تقنيات البرمجة غير المتزامنة (**Asyncio**).

## ✨ المميزات
* **سرعة جنونية:** تعتمد على `aiohttp` و `asyncio` للتعامل مع آلاف الطلبات في وقت قياسي.
* **متعددة المهام:** تدعم فحص المجلدات (Dir) والنطاقات الفرعية (Subdomain) في أداة واحدة.
* **سهولة التثبيت:** تعمل مباشرة عبر بايثون و Git.

## 🛠 التثبيت (Installation)

استخدم **Git** للحصول على الأداة على جهازك (Parrot OS, Kali, or any OS):

```bash
# استنساخ المستودع
git clone https://github.com/DKHEL-ALDOSRY/fast-fuzzer.git

# الدخول للمجلد
cd fast-fuzzer

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt
```

## 🚀 طريقة الاستخدام (Usage)

يمكنك تشغيل الأداة مباشرة باستخدام بايثون:

```bash
#for dir descavry
python3 fuzzer.py -m dir -u http://example.com -w wordlist.txt

#for subdomin descavry
python3 fuzzer.py -m domin -u http://example.com -w wordlist.txt

#for timeout (defolt is 5)
-t 10

# for threads (defolt is 50)
-T 30

#for extunions
-x .php .html .txt 

```

---
👨‍💻 **تطوير:** [DKHEL-ALDOSRY](https://github.com/DKHEL-ALDOSRY)
