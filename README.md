# Boston Condo Explorer

## To Workon

```
mkvirtualenv -p python3 boston_condo_explorer

pip install -r requirements.txt
```

```
celery -A boston_condo_explorer worker -l info
```
http://127.0.0.1:8000/api/mls_complete/?active=True&min_living_area=700&page=2
