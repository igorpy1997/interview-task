include .env
export

ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif

app-dir = addons
odoo-dir = odoo
config-dir = config
data-dir = data
logs-dir = logs

.PHONY: init-submodule
init-submodule:
	@echo "🔗 Adding Odoo as git submodule..."
	git submodule add --branch 18.0 https://github.com/odoo/odoo.git odoo
	git submodule update --init --recursive
	@echo "✅ Odoo submodule added successfully!"

.PHONY: create-dirs
create-dirs:
	@echo "📁 Creating project directories..."
	mkdir -p $(app-dir)
	mkdir -p $(config-dir)
	mkdir -p $(data-dir)/postgres
	mkdir -p $(data-dir)/odoo
	mkdir -p $(data-dir)/redis
	mkdir -p $(logs-dir)
	@echo "✅ Directories created!"

.PHONY: setup-env
setup-env:
	@echo "⚙️ Setting up environment..."
	cp .env.example .env 2>/dev/null || true
	@echo "✅ Environment configured!"

.PHONY: init
init: init-submodule

.PHONY: setup
setup: init create-dirs setup-env
	@echo "🎉 Full project setup completed!"

.PHONY: pull
pull:
	@echo "📥 Updating project and submodules..."
	git pull origin main
	git submodule update --init --recursive
	uv sync --all-extras
	@echo "✅ Project updated successfully!"

.PHONY: update-odoo
update-odoo:
	@echo "🔄 Updating Odoo submodule..."
	cd odoo && git fetch origin && git checkout 18.0 && git pull origin 18.0
	git add odoo
	git commit -m "Update Odoo submodule" || true
	@echo "✅ Odoo submodule updated!"


.PHONY: up
up:
ifeq ($(DETECTED_OS),Windows)
	docker compose \
		--env-file .env \
		--file docker-compose.yml \
		up \
		-d \
		--build \
		--timeout 60 \
		odoo postgres
else
	docker compose \
		--env-file .env \
		--file docker-compose.yml \
		build \
		--build-arg USER_ID=$(SUDO_UID) \
		--build-arg GROUP_ID=$(SUDO_GID) \
		--build-arg USER_NAME=$(SUDO_USER) \
		odoo postgres

	docker compose \
		--env-file .env \
		--file docker-compose.yml \
		up \
		-d \
		--timeout 60 \
		odoo postgres
endif

.PHONY: up-db
up-db:
	docker compose \
		--env-file .env \
		--file docker-compose.yml \
		up \
		-d \
		postgres

.PHONY: build
build:
	docker compose \
		--env-file .env \
		--file docker-compose.yml \
		build \
		odoo

.PHONY: down
down:
	docker compose down

.PHONY: restart
restart: down up

.PHONY: logs
logs:
	docker compose logs -f

.PHONY: logs-odoo
logs-odoo:
	docker compose logs -f odoo

.PHONY: logs-postgres
logs-postgres:
	docker compose logs -f postgres

.PHONY: shell
shell:
	docker compose exec odoo bash

.PHONY: psql
psql:
	docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

.PHONY: backup-db
backup-db:
	@echo "🗄️ Creating database backup..."
	mkdir -p backups
	docker compose exec postgres pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created successfully!"

.PHONY: restore-db
restore-db:
	@echo "🔄 Restoring database..."
	@read -p "Enter backup file path: " backup_file; \
	docker compose exec -T postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) < $$backup_file
	@echo "✅ Database restored successfully!"

.PHONY: clean
clean:
	@echo "🧹 Cleaning up..."
	docker compose down -v
	docker system prune -f
	@echo "✅ Cleanup completed!"

.PHONY: reset
reset: clean
	@echo "🔄 Resetting all data..."
	rm -rf $(data-dir)/postgres/*
	rm -rf $(logs-dir)/*
	@echo "✅ Reset completed!"

.PHONY: install-addon
install-addon:
	@read -p "Enter addon name: " addon_name; \
	docker compose exec odoo odoo -d $(POSTGRES_DB) -i $$addon_name --stop-after-init

.PHONY: upgrade-addon
upgrade-addon:
	@read -p "Enter addon name: " addon_name; \
	docker compose exec odoo odoo -d $(POSTGRES_DB) -u $$addon_name --stop-after-init

.PHONY: scaffold
scaffold:
	@read -p "Enter addon name: " addon_name; \
	docker compose exec odoo odoo scaffold $$addon_name /mnt/extra-addons/

.PHONY: test
test:
	@read -p "Enter addon name: " addon_name; \
	docker compose exec odoo python -m pytest /mnt/extra-addons/$$addon_name/tests/ -v

.PHONY: sync
sync:
	@echo "📦 Syncing dependencies with uv..."
	uv sync --all-extras
	@echo "✅ Dependencies synced!"

.PHONY: lint
lint:
	@echo "🔍 Running ruff linting..."
	uv run ruff check addons/ --fix
	@echo "✅ Linting completed!"

.PHONY: format
format:
	@echo "🎨 Formatting code..."
	uv run black addons/
	uv run isort addons/
	@echo "✅ Formatting completed!"

.PHONY: mypy
mypy:
	@echo "🔬 Running MyPy type checking..."
	uv run mypy addons/
	@echo "✅ Type checking completed!"

.PHONY: test-local
test-local:
	@echo "🧪 Running tests locally..."
	uv run pytest addons/ -v
	@echo "✅ Local tests completed!"

.PHONY: dev
dev: up
	@echo "🚀 Development environment started!"
	@echo "📊 Odoo: http://localhost:8069"
	@echo "🗄️ Database: localhost:5432"
	@echo "📧 Default login: admin / admin"

%::
	@exit 0