from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)

client = Client("Qwen/Qwen2.5-72B-Instruct")
system_message = "Sen bir AI asistanısın ve tek görevin Aritmi hakkında kullanıcıyı bilgilendirmek ve kullanıcının kalp ritim bozukluğu, kalp atışı, aritmi riski, vücut sıcaklığı ve terleme durumlarını inceleyerek kullanıcıya yapması gerekenler hakkında tavsiyeler vermek. Eğer kullanıcının aritmi riski varsa, aritmi geçiriyorsa veya hastalığın atağını geçiriyorsa tavsiyeler ver ve ne yapması gerektiğini anlat. Bu konuların dışına asla çıkamazsın."

# Kullanıcı IP adreslerine göre history tutan bir sözlük
user_histories = {}

@app.route("/chat", methods=["POST"])
def chat():
    user_ip = request.remote_addr  # Kullanıcı IP adresini al
    if user_ip not in user_histories:
        user_histories[user_ip] = []  # IP için yeni bir history başlat
    
    history = user_histories[user_ip]  # Bu IP için history
    user_input = request.json.get("message")
    
    if user_input.lower() == 'exit':
        user_histories.pop(user_ip, None)  # Kullanıcı çıkış yaparsa history temizlenir
        return jsonify({"response": "Konuşma bitiriliyor..."})
    
    result = client.predict(
        query=user_input,
        history=history,
        system=system_message,
        api_name="/model_chat"
    )
    
    bot_response = result[1][len(history)][1]
    history.append((user_input, bot_response))
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
