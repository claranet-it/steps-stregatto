black:
	black ./core/cat/plugins/portfolio_tool

isort:
	isort ./core/cat/plugins/portfolio_tool --profile black

qa: black isort

test-filter:
	docker exec portfolio_cheshire_cat python -m pytest ${filter} --color=yes .

test:
	docker exec portfolio_cheshire_cat python -m pytest --color=yes .