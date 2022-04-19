from requests import get, post, delete



print(delete('http://localhost:5000/api/wishes/5').json())
print(delete('http://localhost:5000/api/wishes/7').json())
print(delete('http://localhost:5000/api/wishes/8').json())
print(delete('http://localhost:5000/api/wishes/9').json())
print(delete('http://localhost:5000/api/wishes/10').json())
print(delete('http://localhost:5000/api/wishes/11').json())