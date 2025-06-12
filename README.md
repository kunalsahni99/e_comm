1. To run the the docke container using the pulled Redis image:
docker run --name django-redis -d -p 6379:6379 --rm redis

2. To start the Redis bash:
docker exec -ti <Contasiner_ID> bash

3. To run the Redis CLI:
redis-cli -n 1

4. To flush the Redis cache:
flushdb

5. To start the celery worker:
celery -A <Name_of_the_app> worker --loglevel=INFO