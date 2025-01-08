# a kiinduló image megadása
FROM python:3.13-slim

# a munkakönyvtár definiálása a konténeren belül
WORKDIR /app

# új felhasználó (app) létrehozása
RUN addgroup app && adduser --system -ingroup app app

# szükséges fájlok felmásolása a konténerbe
# python függőségek telepítése a konténeren belül
COPY requirements.txt requirements.txt

# a szükséges csomagok telempítése a konténeren belül
RUN pip install -r requirements.txt

# szükséges fájlok felmásolása a konténerbe
# .dockerignore -> kivétel fel van sorolva
COPY . .

# jogok beállítása (az app-hoz)
RUN chown -R app:app /app
RUN chmod 755 /app

#átlépés az app felhasználóra
USER app

# konténer portjának megadása
#EXPOSE 8000

# konténer indításakor futtatandó parancs
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8800" ]