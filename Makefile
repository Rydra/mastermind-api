build:
	DOCKER_BUILDKIT=1 docker build -f compose/local/django/Dockerfile . -t mastermind_py_local_django --force-rm --compress

up:
	docker-compose --profile app --profile infra up --remove-orphans --quiet-pull

up-debug:
	docker-compose --profile debug --profile infra up --remove-orphans --quiet-pull

down:
	docker-compose down --remove-orphans

run-tests:
	docker-compose run --rm django pytest

run-infrastructure:
	docker-compose --profile infra up

check:
	pre-commit run --all-files
