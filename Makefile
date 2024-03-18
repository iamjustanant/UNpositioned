dev:
	cd backend && flask run --host=0.0.0.0 --port=5000

client-dev:
	cd backend/client && npm install && npm run dev

client-build:
	cd backend/client && npm install && npm run build