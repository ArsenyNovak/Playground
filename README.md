PLAYGROUNDS
===


My pet projects about playgrounds in Minsk


## Technologies
Python, Django, DjangoRestFramework  
Docker

## Local setup
---
1. Run command: git clone https://github.com/ArsenyNovak/Playground.git
2. Work directory create file ".env":  
   #.env
   
   #key for Django  
  SECRET_KEY=your_secret_key  
  DEBUG=True

   #key for db  
  DB_NAME=db  
  DB_USER=your_name  
  DB_PASSWORD=your_password  
  DB_HOST=dbps  
  DB_PORT=5432

   #key for SNTP-server (yandex.ru)   
  EMAIL_HOST_PASSWORD=your_email_password  
  EMAIL_HOST_USER=your_host_email  
  RECIPIENTS_EMAIL=your_recipients_email  
3. Run command: docker compose up --build
4. Run command: docker compose exec Django python manage.py migrate
5. Run command: docker compose exec Django python manage.py createsuperuser  
   (enter: login, mail, password)
6. Run command: docker compose exec Django python manage.py loaddata playgrounds.json
