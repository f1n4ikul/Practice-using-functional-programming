from flask import Flask, request, jsonify
import sqlite3
import shortuuid

app = Flask(__name__)
DATABASE = 'urls.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (short_url TEXT PRIMARY KEY, normal_url TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['POST'])
def create_short_url():
    data = request.json
    normal_url = data.get('normal_url')
    if not normal_url:
        return jsonify({'error': 'Missing normal_url'}), 400
    
    short_url = shortuuid.ShortUUID().random(length=6)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO urls (short_url, normal_url) VALUES (?, ?)",
                  (short_url, normal_url))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'URL already exists'}), 409
    finally:
        conn.close()
    
    return jsonify({'short_url': short_url}), 201

@app.route('/<short_url>', methods=['GET'])
def get_normal_url(short_url):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT normal_url FROM urls WHERE short_url=?", (short_url,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return jsonify({'normal_url': result[0]})
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/<short_url>', methods=['PUT'])
def update_url(short_url):
    data = request.json
    new_normal_url = data.get('normal_url')
    if not new_normal_url:
        return jsonify({'error': 'Missing normal_url'}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE urls SET normal_url=? WHERE short_url=?",
              (new_normal_url, short_url))
    if c.rowcount == 0:
        conn.close()
        return jsonify({'error': 'URL not found'}), 404
    conn.commit()
    conn.close()
    return jsonify({'message': 'URL updated successfully'})

@app.route('/<short_url>', methods=['DELETE'])
def delete_url(short_url):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM urls WHERE short_url=?", (short_url,))
    if c.rowcount == 0:
        conn.close()
        return jsonify({'error': 'URL not found'}), 404
    conn.commit()
    conn.close()
    return jsonify({'message': 'URL deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(port=5000)