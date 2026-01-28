# 🛒 Shop Project

Интернет-магазин  
Backend: Django + DRF  
Frontend: Nuxt 4  

---

## 🚀 Запуск backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
