To run the the docke container using the pulled Redis image:
docker run --name django-redis -d -p 6379:6379 --rm redis