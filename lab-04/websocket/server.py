import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)
        print("WebSocket opened")

    def on_close(self):
        WebSocketServer.clients.remove(self)
        print("WebSocket closed")

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client in cls.clients:
            try:
                client.write_message(message)
            except:
                pass

class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application([
        (r"/websocket", WebSocketServer),
    ])
    
    # Lưu ý: Trong ảnh client kết nối port 9090, nên ta để server listen 9090
    app.listen(9090) 

    io_loop = tornado.ioloop.IOLoop.current()
    
    word_selector = RandomWordSelector(['apple', 'banana', 'orange', 'grape', 'melon'])

    # Gửi tin nhắn mỗi 3 giây (3000ms)
    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()), 3000
    )
    
    periodic_callback.start()
    
    print("Server started on port 9090...")
    io_loop.start()

if __name__ == "__main__":
    main()