from flask import Flask, jsonify

app = Flask(__name__)

posts = [
    {
        "id": 1,
        "title": "Hacking Etico",
        "image": "https://media.istockphoto.com/id/1144604245/photo/a-computer-system-hacked-warning.jpg?s=612x612&w=0&k=20&c=U45FHOm5rflXIRqmYByxlQANtdtycEdFZz2Vp5dgI8E=",
        "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
    },
    {
        "id": 2,
        "title": "Hacking Web con IA",
        "image": "https://www.simplilearn.com/ice9/free_resources_article_thumb/ethicalhacking.jpg",
        "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
    }
]

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

if __name__ == '__main__':
    app.run(port=80)

