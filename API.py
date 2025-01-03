from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)

client = Client("Qwen/Qwen2.5-72B-Instruct")
system_message = "Sen bir AI asistanısın ve tek görevin Pheochromocytoma hakkında kullanıcıyı bilgilendirmek ve kullanıcının kalp ritim bozukluğu, kalp atışı, aritmi riski, vücut sıcaklığı ve terleme durumlarını inceleyerek kullanıcıya yapması gerekenler hakkında tavsiyeler vermek. Eğer kullanıcının aritmi riski varsa, aritmi geçiriyorsa veya hastalığın atağını geçiriyorsa tavsiyeler ver ve ne yapması gerektiğini anlat. Bu konuların dışına asla çıkamazsın."

history = []

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if user_input.lower() == 'exit':
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
