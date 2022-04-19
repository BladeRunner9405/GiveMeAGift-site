from requests import get, post, delete

print(get('http://localhost:5000/api/wishes/1').json())

print(get('http://localhost:5000/api/wishes/999').json())
print(get('http://localhost:5000/api/wishes/q').json())

print(post('http://localhost:5000/api/wishes').json())

print(post('http://localhost:5000/api/wishes',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:5000/api/wishes',
           json={'title': 'Заголовок',
                 'description': 'Текст новости',
                 'user_id': 1}).json())

print(delete('http://localhost:5000/api/wishes/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/wishes/6').json())