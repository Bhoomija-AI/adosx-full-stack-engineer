\# AdosX Full-Stack Engineer – Discrepancy Dashboard



A full-stack discrepancy dashboard built for the AdosX Engineering take-home assignment.



\## Tech Stack



\* Backend: Django, Django REST Framework

\* Frontend: React, Vite

\* Database: SQLite

\* Data: CSV files



\## Features



\* View reconciliation discrepancies by organization

\* Filter discrepancies by reason

\* View record ID, location, System A value and System B value

\* Refresh discrepancy data

\* Loading and error states

\* Backend API with automated tests



\## Project Structure



```text

backend/

&#x20; core/

&#x20; reconciler/

&#x20; manage.py

&#x20; requirements.txt



frontend/

&#x20; src/

&#x20; package.json



data/

&#x20; locations.csv

&#x20; system\_a.csv

&#x20; system\_b.csv

```



\## Backend Setup



```bash

cd backend

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

```



Backend API:



```text

http://127.0.0.1:8000/api/discrepancies/

```



\## Frontend Setup



Open a new terminal:



```bash

cd frontend

npm install

npm run dev

```



Frontend:



```text

http://localhost:5173/

```



\## Run Tests



From the backend folder:



```bash

python manage.py test reconciler

```



\## Organizations



The dashboard supports:



\* ORG-A

\* ORG-B



\## Author



Bhoomija



