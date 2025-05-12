from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_books(query, genre):
    if genre:
        query += f"+subject:{genre}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json()
    books = []
    for item in data.get('items', [])[:10]:
        volume = item['volumeInfo']
        books.append({
            'title': volume.get('title', 'No Title'),
            'authors': ", ".join(volume.get('authors', ['Unknown Author'])),
            'description': volume.get('description', 'No Description Available'),
            'thumbnail': volume.get('imageLinks', {}).get('thumbnail', ''),
            'link': volume.get('previewLink', '#'),
            'rating': volume.get('averageRating'),
            'ratingsCount': volume.get('ratingsCount')
        })
    return books

@app.route("/", methods=["GET", "POST"])
def index():
    books = []
    query = ""
    genre = ""
    if request.method == "POST":
        query = request.form.get("query")
        genre = request.form.get("genre")
        if query:
            books = get_books(query, genre)
    return render_template("index.html", books=books, query=query, genre=genre)

if __name__ == "__main__":
    app.run(debug=True)
