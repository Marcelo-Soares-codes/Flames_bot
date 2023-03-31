import requests
from telebot import TeleBot

class ApiDouble():
    def __init__(self):
        self.url = "https://www.flames.bet/api/row_double_game/latest_term"
        self.response = requests.get(self.url)

        if self.response.status_code == 200:
            self.data = self.response.json()["model"]

        else:
            print(f"Certifique-se de que está conectado à internet ou faça uma busca para saber o motivo do código recebido: {self.response.status_code}")
            self.data = {}
        
    def waiting(self):  # Aguarda finalizar o giro para retornar os dados que foram coletados
        while self.data["status"] == "FINISHED":
            self.data = requests.get(self.url).json()["model"]
        while self.data["status"] != "FINISHED":
            self.data = requests.get(self.url).json()["model"]
        return self.data

    def last_number(self):  # Retorna o ultimo numero que saiu na plataforma
        if self.data["status"] == "FINISHED": 
            return self.data["number"]
            
    def last_color(self):  # Retorna o ultima cor que saiu na plataforma
        if self.data["status"] == "FINISHED": 
            return self.data["color"]
    
    def last_bet_amount(self):  # Retorna o ultimo numero que s
        if self.data["status"] == "FINISHED": 
            return self.data["betAmount"]

class Bot(): 
    def __init__(self):
        token = "6060820498:AAFQJy1ol0TZdIegzFfbrneMIVPM5Iumu4o"  # Aqui deve ser inserido o token do seu bot
        self.chat_id = "-1001953178343"  # Aqui deve ser inserido o chat id do seu bot
        self.bot = TeleBot(token=token)
        self.bot.send_message(self.chat_id, "🤖 Robot Starting")

        self.last_numbers = []
        self.last_colors = []
        self.black_patterns = [
["red","red","red","red","red"],
["black","black","red","red"],
["black","red","black","red"],
["red","black","black","red"],
["black","black","red","black"],
["black","red","red","red"]]  # Aqui deve ser adicionado os padroes em lista que o bot enviara o sinal para a cor preta ex: self.standards = [["red","red","black","black","red"], ["red","red","red","red"]]. OBS: os podrões devem conter ate no maximo 10 cores
        
        self.red_patterns = [
["black","black","black","black","black"],
["red","red","black","black"],
["red","black","red","black"],
["black","red","red","black"],
["red","red","black","red"],
["red","black","black","black"]]  # Aqui deve ser adicionado os padroes em lista que o bot enviara o sinal para a cor vermelha ex: self.standards = [["black","black","red","red","black"], ["black","black","black","black",]]. OBS: os podrões devem conter ate no maximo 10 cores

    def limit_lists(self, num, color):  # Limita as ultimas "pedras" que sairam a 10 e retorna os ultimos 10 numero e as ultimas 10 cores
        if len(self.last_numbers) >= 10:
            self.last_numbers.pop(0)
        if len(self.last_colors) >= 10:
            self.last_colors.pop(0)
        self.last_numbers.append(num)
        self.last_colors.append(color)
        print(self.last_colors)
        return self.last_numbers, self.last_colors

    def check_patterns(self, colors, last_num, last_color):  # Checa o padrão e envia o sinal. Recebe uma lista das ultimas cores, o ultimo numero e cor, e retorna um verdadeiro se enviar o sinal
        for pattern in self.black_patterns:
            pattern_size = len(colors) - len(pattern)
            if pattern == colors[pattern_size:]:
                self.bot.send_message(self.chat_id ,f"✅entrada no Preto --> ⚫ \nConfirmada Após {last_num} [{last_color}]")
                return "black"

        for pattern in self.red_patterns:
            pattern_size = len(colors) - len(pattern)
            if pattern == colors[pattern_size:]:
                self.bot.send_message(self.chat_id ,f"✅entrada no Vermelho --> 🔴 \nConfirmada Após {last_num} [{last_color}]")
                return "red"

    def check_victory(self, signal_color, last_color, gale):
        if signal_color == last_color or last_color == "white":
            if signal_color == last_color:
                if gale == 0:
                    self.bot.send_message(self.chat_id, f"✅✅✅ Victory sg ✅✅✅")
                if gale == 1:
                    self.bot.send_message(self.chat_id, f"✅✅✅ Victory g1 ✅✅✅")
                if gale == 2:
                    self.bot.send_message(self.chat_id, f"✅✅✅ Victory g2 ✅✅✅")
            else:
                self.bot.send_message(self.chat_id, f"⚪⚪⚪ White ⚪⚪⚪")
            return True
        else:
            if gale >= 2:
                self.bot.send_message(self.chat_id, f"🔺🔺🔺 Loss 🔺🔺🔺")
            return False

api = ApiDouble()
bot = Bot()
while True:
    api.waiting()
    last_num = api.last_number()
    last_color = api.last_color()

    list_numbers, list_colors = bot.limit_lists(num=last_num, color=last_color)
    signal_color = bot.check_patterns(colors=list_colors, last_num=last_num, last_color=last_color)
    if signal_color:
        for martingale in range(3):  # Aqui é a quantidade de martingale
            api.waiting()
            last_color = api.last_color()
            last_num = api.last_number()
            bot.limit_lists(num=last_num, color=last_color)
            if bot.check_victory(signal_color, last_color, martingale):
                break



