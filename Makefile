build:
	docker-compose -f docker-compose-debug.yml build

debug:
	docker-compose -f docker-compose-debug.yml up

up:
	docker-compose up -d
	docker-compose logs -f

down:
	docker-compose down

watch:
	./node_modules/webpack/bin/webpack.js --watch --progress --colors

index:
	docker exec -it searchjupyter_search_1 python3 /usr/src/app/search/indexer.py -d /notebooks

reset:
	# Delete the elastic search index forcing a rebuild
	docker exec -it searchjupyter_es_1 curl -X DELETE localhost:9200/jupyter

test:
	docker exec -it searchjupyter_search_1 py.test -p no:cacheprovider -s -x
