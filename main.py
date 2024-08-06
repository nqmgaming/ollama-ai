from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import ollama

app = Flask(__name__)
app.secret_key = 'minh'  # Dùng để bảo mật session trong Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Mô hình cơ sở dữ liệu
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)


# Tạo cơ sở dữ liệu
with app.app_context():
    db.create_all()


@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get('user_id')
    user_input = request.json.get('message')

    # Kiểm tra và lưu câu hỏi của người dùng
    if user_id:
        # Lưu câu hỏi của người dùng vào cơ sở dữ liệu
        db.session.add(Conversation(user_id=user_id, role='user', content=user_input))
        db.session.commit()

        # Lấy lịch sử cuộc trò chuyện từ cơ sở dữ liệu
        conversation_history = Conversation.query.filter_by(user_id=user_id).all()
        messages = [{'role': conv.role, 'content': conv.content} for conv in conversation_history]

        # Gửi lịch sử cuộc trò chuyện cùng với yêu cầu mới đến mô hình
        stream = ollama.chat(
            model='phi3:latest',
            messages=messages,
            stream=True,
        )

        response_content = ''
        for chunk in stream:
            response_content += chunk['message']['content']

        # Lưu phản hồi của mô hình vào cơ sở dữ liệu
        db.session.add(Conversation(user_id=user_id, role='assistant', content=response_content))
        db.session.commit()

        return jsonify({'response': response_content})

    return jsonify({'error': 'User ID and message are required'}), 400


if __name__ == "__main__":
    app.run()
