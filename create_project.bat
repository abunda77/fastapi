@echo off
:: Membuat direktori
mkdir app
mkdir app\api
mkdir app\api\v1
mkdir app\core
mkdir app\db
mkdir app\schemas

:: Membuat file kosong di setiap direktori
cd app\api\v1
type nul > __init__.py
type nul > auth.py
type nul > users.py
type nul > properties.py
cd ..\..\..

cd app\core
type nul > config.py
type nul > security.py
type nul > dependencies.py
cd ..\..

cd app\db
type nul > __init__.py
type nul > base.py
type nul > models.py
cd ..\..

cd app\schemas
type nul > __init__.py
cd ..\..

cd app
type nul > main.py
cd ..

type nul > requirements.txt
type nul > .env

echo Struktur direktori dan file telah dibuat.
pause
