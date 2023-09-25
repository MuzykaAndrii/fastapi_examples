up:
	docker compose -f docker-compose-dev.yml up -d --build

down:
	docker compose -f docker-compose-dev.yml down

test:
	docker exec -t backend pytest -v -s -W ignore::DeprecationWarning

pre-commit:
	poetry run pre-commit run --show-diff-on-failure --color=always --all-files

logs:
	docker logs --follow backend