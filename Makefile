bash:
	docker-compose run --volume ~/.aws/:/root/.aws/ --rm app bash

build:
	docker-compose build

test:
	docker-compose run --volume ~/.aws/:/root/.aws/ --rm app pytest --cov-report term