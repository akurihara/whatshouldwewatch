# whichflix

```
docker build -t alexkurihara/whatshouldwewatch .
```
```
docker run -p 8000:8000 --env-file .env.docker alexkurihara/whatshouldwewatch
```
```
docker run -it alexkurihara/whatshouldwewatch sh
```
```
python whichflix/manage.py test test/path/to/file
```
