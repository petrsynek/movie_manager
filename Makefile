export APP_PORT?=8080

build:
	docker compose build

up:
	REMOTE_API_URL=https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json \
	REMOTE_API_POLL_INTERVAL=100 \
	MONGO_URI=mongodb://mongo:27017/movie_db \
	RESET_DB=false \
	docker compose up -d

	@echo -e "\n================================================ \n App is running at http://localhost:$(APP_PORT) \n ===============================================\n"

down:
	docker compose down

test:
	REMOTE_API_URL=http://localhost:8090/external_data \
	REMOTE_API_POLL_INTERVAL=1 \
	MONGO_URI=mongodb://mongo:27017/test \
	RESET_DB=true \
	docker compose up -d
	docker compose exec -w /movie_manager movie_manager pytest tests
	docker compose down
