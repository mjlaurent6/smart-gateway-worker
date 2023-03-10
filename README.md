## Backend Worker

Build

`docker build -t backend-worker .`

Run dev

`docker run -p 8000:80 backend-worker`

Run prod

`docker run -dp 8000:80 backend-worker`


Copy .env

`scp .env lab2@143.89.144.31:~/deploy-test/`