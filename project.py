import random
import telebot
from os import getenv
from telebot import types
from time import sleep
from dotenv import load_dotenv


load_dotenv()
api_key = getenv("API_KEY")
bot = telebot.TeleBot(api_key)

robots = [{"id": "1", "title": "Shelem Game", "description": "play shelem game\nwith 1 to 4 players", "thumb": "https://i.imgur.com/JdnG6KF.jpg", "message": "Who wants to play Shelem😃? Press the button to join!\n\nCurrent players:"}]

cards= {1:"A♠️",2:"K♠️",3:"Q♠️",4:"J♠️",5:"10♠️",6:"9♠️",7:"8♠️",8:"7♠️",9:"6♠️",10:"5♠️",11:"4♠️",12:"3♠️",13:"2♠️",
       14:"A♥️",15:"K♥️",16:"Q♥️",17:"J♥️",18:"10♥️",19:"9♥️",20:"8♥️",21:"7♥️",22:"6♥️",23:"5♥️",24:"4♥️",25:"3♥️",26:"2♥️",
       27:"A♣️",28:"K♣️",29:"Q♣️",30:"J♣️",31:"10♣️",32:"9♣️",33:"8♣️",34:"7♣️",35:"6♣️",36:"5♣️",37:"4♣️",38:"3♣️",39:"2♣️",
       40:"A♦️",41:"K♦️",42:"Q♦️",43:"J♦️",44:"10♦️",45:"9♦️",46:"8♦️",47:"7♦️",48:"6♦️",49:"5♦️",50:"4♦️",51:"3♦️",52:"2♦️"}
card_numbers = [i for i in range(1,53)]

class Player:
    def __init__(self, user_id, first_name, user_name) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.user_name = user_name
        self._cards = []

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards: list):
        if len(cards) > 12:
            raise ValueError("Number of cards is too much")
        self._cards = cards
    
    # def card(self, card_dict, i):
    #     return card_dict[self.cards[i]]
    def display_name(self):
        return f"<a href='tg://user?id={self.user_id}'>{self.first_name}</a>"



class Group:
    def __init__(self, player1: Player, player2: Player, color) -> None:
        self.player1 = player1
        self.player2 = player2
        self._cards = []
        self.color = color

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards: list):
        self._cards = cards
    
    @property
    def win_round(self):
        return len(self.cards) // 4

    @win_round.setter
    def win_round(self, win_round):
        pass
    
    @property
    def player_ids(self):
        return [self.player1.user_id, self.player2.user_id]
    
    @player_ids.setter
    def player_ids(self, player_ids):
        pass

    @property
    def color_team(self):
        if self.color == "🔴":
            return "Red team"
        return "Blue team"

    @color_team.setter
    def color_team(self, color_team):
        pass

    def group_score(self):
        score = (len(self.cards) // 4) * 5
        for i in self.cards:
            if i % 13 == 1 or i % 13 == 5:
                score += 10
            elif i % 13 == 10:
                score += 5
        return score

class Game:
    ID = 0
    def __init__(self, players:list=None, players_id:set=None, scoring_id:list=None, ruler:Player=None, rule:list=None, 
                 rule_sign:str=None, group1:list=None, group2:list=None, ruler_group:Group=None, 
                 another_group:Group=None, current_rule:list=None, played_cards:dict=None,
                 final_score:int=0, turn:int=None, answer:dict=None, score:int=95,
                 this_turn:int=None) -> None:
        self.players = players if players is not None else []
        self.players_id = players_id if players_id is not None else set()
        self.scoring_id = scoring_id if scoring_id is not None else []
        self.ruler = ruler
        self.rule = rule if rule is not None else []
        self.rule_sign = rule_sign if rule_sign is not None else ""
        self.group1 = group1 if group1 is not None else []
        self.group2 = group2 if group2 is not None else []
        self.ruler_group = ruler_group
        self.another_group = another_group
        self.current_rule = current_rule if current_rule is not None else []
        self.played_cards = played_cards if played_cards is not None else {}
        self.final_score = final_score
        self.turn = turn
        self.answer = answer if answer is not None else {}
        self.score = score
        self.this_turn = this_turn
        self.id = Game.get_id()
    
    @staticmethod
    def get_id():
        Game.ID += 1
        return Game.ID - 1

games: dict[int, Game] = {}

def main():
    @bot.inline_handler(func= lambda query: len(query.query) == 0)
    def handel_inline_query(query):
        # global game
        # game = Game()
        # games[g.id] = game
        # user_id = query.from_user.id
        # first_name = str(query.from_user.first_name).split()[0]
        # user_name = query.from_user.username
        # games[g.id].players.append(Player(user_id, first_name, f"@{user_name}"))
        # games[g.id].players_id.add(user_id)
        # display_name1  = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
        results = []
        keyboard_lets_play = lets_play()
        for robot in robots:
            result = types.InlineQueryResultArticle(
                id=robot["id"],
                title=robot["title"],
                description=robot["description"],
                input_message_content=types.InputTextMessageContent(
                    message_text= f"Who wants to play Shelem😃? Press the button to join!\n\nCurrent players:" ,
                    parse_mode="HTML"
                ),
                thumbnail_url=robot["thumb"],
                reply_markup=keyboard_lets_play
            )
            results.append(result)

        bot.answer_inline_query(query.id, results)


    
    # @bot.callback_query_handler(func=lambda call: call.data in ["join_game", "start_game"])
    @bot.callback_query_handler(func=lambda call: call.data =="join_game")
    def join_game(call):
        global g
        try:
            g
        except:
            g = Game()
            games[g.id] = g
        if call.data == "join_game" and call.from_user.id not in games[g.id].players_id:
            user_id = call.from_user.id
            first_name = str(call.from_user.first_name).split()[0]
            username = call.from_user.username
            games[g.id].players.append(Player(user_id, first_name, f"@{username}"))
            games[g.id].players_id.add(user_id)
            text = "Who wants to play Shelem😃? Press the button to join!\n\nCurrent players:\n"
            for p in games[g.id].players:
                text += f"{p.display_name()}\n"
            keyboard_lets_play = lets_play()
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text, reply_markup= keyboard_lets_play, parse_mode="HTML")
            bot.answer_callback_query(call.id)
        elif call.data == "join_game" and call.from_user.id in games[g.id].players_id:
            bot.answer_callback_query(call.id, "You already join")

        # if len(games[g.id].players_id) == 4 or call.data == "start_game":
        if len(games[g.id].players_id) == 4:
            # while len(games[g.id].players) != 4:
            #     games[g.id].players.append(Player(" ", " ", " "))
            print(len(games[g.id].players))
            games[g.id].group1, games[g.id].group2 = make_groups(games[g.id].players)
            print(len(games[g.id].players))
            print(games[g.id].group1, games[g.id].group2)
            deal_cards(card_numbers, games[g.id].players)
            ruling1 = calling_score(games[g.id].players, games[g.id].score, p1_s="finger")
            text = f"Shelem game\n\n🔵:{games[g.id].group1[0].first_name} and {games[g.id].group1[1].first_name}\n🔴:{games[g.id].group2[0].first_name} and {games[g.id].group2[1].first_name}\n\n{games[g.id].players[0].display_name()} Read your hand and say the score you might get"
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text, reply_markup= ruling1, parse_mode="HTML")
            bot.answer_callback_query(call.id)
            for player in games[g.id].players:
                games[g.id].scoring_id.append(player.user_id)
            # playing_id = games[g.id].scoring_id.copy()
            games[g.id].turn = games[g.id].scoring_id[0]
            games[g.id].answer = {games[g.id].players[0].user_id:" ", games[g.id].players[1].user_id:" ", games[g.id].players[2].user_id:" ", games[g.id].players[3].user_id:" "}
            print(f"11111111{games[g.id].scoring_id, games[g.id].turn, games[g.id].score, games[g.id].answer}111111111111")

    @bot.callback_query_handler(func= lambda call: call.data in["pass_1","score1_100","score1_105","score1_110","score1_115","score1_120","score1_125","score1_130","score1_135","score1_140","score1_145","score1_150","score1_155","score1_160","score1_165"])
    def call_score(call):
        global g
        display = ""
        games[g.id].this_turn = 0
        print(f"11111111{games[g.id].scoring_id, games[g.id].turn, games[g.id].score, games[g.id].answer}111111111111")
        print(call.from_user.id, type(call.from_user.id))
        if call.from_user.id == games[g.id].turn:
            games[g.id].this_turn = games[g.id].turn
            is_pass = False
            if call.data == "pass_1":
                games[g.id].answer[games[g.id].turn] = "pass"
                is_pass = True
            else:
                games[g.id].score = int(call.data[-3:])
                games[g.id].answer[games[g.id].turn] = games[g.id].score

            turn_index = (games[g.id].scoring_id.index(games[g.id].turn) + 1)%len(games[g.id].scoring_id)
            games[g.id].turn = games[g.id].scoring_id[turn_index]
            games[g.id].answer[games[g.id].turn] = "finger"
            for p in games[g.id].players:
                if p.user_id == games[g.id].turn:
                    display = p.display_name()
            games[g.id].final_score = games[g.id].score
            text = f"Shelem game\n\n🔵:{games[g.id].group1[0].first_name} and {games[g.id].group1[1].first_name}\n🔴:{games[g.id].group2[0].first_name} and {games[g.id].group2[1].first_name}\n\n{display} Read your hand and say the score you might get"
            ruling = calling_score(games[g.id].players, games[g.id].score, games[g.id].answer[games[g.id].players[0].user_id], games[g.id].answer[games[g.id].players[1].user_id], games[g.id].answer[games[g.id].players[2].user_id], games[g.id].answer[games[g.id].players[3].user_id])
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text, reply_markup= ruling, parse_mode="HTML")
            bot.answer_callback_query(call.id)
            if is_pass:
                games[g.id].scoring_id.remove(call.from_user.id)
        else:
            bot.answer_callback_query(call.id, "it`s not your turn")
        if len(games[g.id].scoring_id) == 1 or (call.data == "score1_165" and call.from_user.id == games[g.id].this_turn):
            if call.data == "score1_165":
                games[g.id].final_score = 165
            if len(games[g.id].scoring_id) == 1:
                games[g.id].this_turn = games[g.id].scoring_id[0]
            for p in games[g.id].players:
                if p.user_id == games[g.id].this_turn:
                    display = p.display_name()
                    global ruler_group, another_group
                    games[g.id].ruler = p
                    if p in games[g.id].group1:
                        games[g.id].ruler_group = Group(games[g.id].group1[0], games[g.id].group1[1], "🔵")
                        games[g.id].another_group = Group(games[g.id].group2[0], games[g.id].group2[1], "🔴")
                        break
                    games[g.id].ruler_group = Group(games[g.id].group2[0], games[g.id].group2[1], "🔴")
                    games[g.id].another_group = Group(games[g.id].group1[0], games[g.id].group1[1], "🔵")
                    break
            games[g.id].turn = games[g.id].ruler.user_id
            print("card_numbers:", card_numbers)
            for card in card_numbers:
                games[g.id].ruler.cards.append(card)
            card_numbers.clear()
            text2 = f"Shelem game\n\n{games[g.id].ruler_group.color}:{games[g.id].ruler_group.player1.first_name} and {games[g.id].ruler_group.player2.first_name}\n{games[g.id].another_group.color}:{games[g.id].another_group.player1.first_name} and {games[g.id].another_group.player2.first_name}\n\n{display} you are the ruller\nsee the 4 remaining cards and dump 4 cards in total.\n\n4 cards remain..."
            ruling = make_rule_button(games[g.id].players, games[g.id].ruler)
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text2, reply_markup= ruling, parse_mode="HTML")
            bot.answer_callback_query(call.id)
            games[g.id].answer.clear()
            games[g.id].answer = {games[g.id].players[0].user_id:" ", games[g.id].players[1].user_id:" ", games[g.id].players[2].user_id:" ", games[g.id].players[3].user_id:" "}
    
    @bot.callback_query_handler(func= lambda call: call.data in["cart1_1","cart1_2","cart1_3","cart1_4","cart1_5","cart1_6","cart1_7","cart1_8","cart1_9","cart1_10","cart1_11","cart1_12","cart1_13","cart1_14","cart1_15","cart1_16"])
    def make_rule(call):
        global g
        if call.from_user.id == games[g.id].ruler.user_id:
            dump_cards(games[g.id].ruler, call.data, call.id, games[g.id].ruler_group)
            text2 = f"Shelem game\n\n{games[g.id].ruler_group.color}:{games[g.id].ruler_group.player1.first_name} and {games[g.id].ruler_group.player2.first_name}\n{games[g.id].another_group.color}:{games[g.id].another_group.player1.first_name} and {games[g.id].another_group.player2.first_name}\n\n{games[g.id].ruler.display_name()} you are the ruller\nsee the 4 remaining cards and dump 4 cards in total.\n\n{4 - len(games[g.id].ruler_group.cards)} cards remain..."
            ruling = make_rule_button(games[g.id].players, games[g.id].ruler)
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text2, reply_markup= ruling, parse_mode="HTML")
            bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, "it`s not your turn")
        
        if len(games[g.id].ruler_group.cards) == 4:
            for item in games[g.id].ruler_group.cards:
                games[g.id].ruler.cards.remove(item)
            games[g.id].ruler.cards.sort()
            games[g.id].answer[games[g.id].ruler.user_id] = "finger"
            text_playing = f"Shelem game\n\n{games[g.id].ruler_group.color}:{games[g.id].ruler_group.player1.first_name} and {games[g.id].ruler_group.player2.first_name}     ...............     {games[g.id].ruler_group.group_score()}/{games[g.id].final_score}\n{games[g.id].another_group.color}:{games[g.id].another_group.player1.first_name} and {games[g.id].another_group.player2.first_name}     ...............     {games[g.id].another_group.group_score()}\n\n{games[g.id].ruler.display_name()} it`s your trun. Play your card."
            playing = playing_shelem(games[g.id].players, games[g.id].ruler, games[g.id].ruler_group, games[g.id].another_group, "?", games[g.id].answer[games[g.id].players[0].user_id], games[g.id].answer[games[g.id].players[1].user_id], games[g.id].answer[games[g.id].players[2].user_id], games[g.id].answer[games[g.id].players[3].user_id])
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text_playing, reply_markup= playing, parse_mode="HTML")


    @bot.callback_query_handler(func= lambda call: call.data in["cart3_1","cart3_2","cart3_3","cart3_4","cart3_5","cart3_6","cart3_7","cart3_8","cart3_9","cart3_10","cart3_11","cart3_12","cart3_13","cart3_14","cart3_15","cart3_16"])
    def playing(call):
        global g
        display = ""   
        if len(games[g.id].ruler.cards) == 12 and call.from_user.id == games[g.id].ruler.user_id and games[g.id].turn == games[g.id].ruler.user_id:
            games[g.id].rule, games[g.id].rule_sign = set_rule(call.data, games[g.id].ruler)
            games[g.id].current_rule = games[g.id].rule
            card_num = card_number(call.data, games[g.id].turn, games[g.id].players)
            games[g.id].played_cards[card_num] = call.from_user.id
            games[g.id].answer[games[g.id].turn] = cards[card_num]
            games[g.id].turn = next_turn(games[g.id].turn, games[g.id].players)
            games[g.id].answer[games[g.id].turn] = "finger"
            for p in games[g.id].players:
                if p.user_id == games[g.id].turn:
                    display = p.display_name()
                    break
            text_playing = f"Shelem game\n\n{games[g.id].ruler_group.color}:{games[g.id].ruler_group.player1.first_name} and {games[g.id].ruler_group.player2.first_name}     ...............     {games[g.id].ruler_group.group_score()}/{games[g.id].final_score}\n{games[g.id].another_group.color}:{games[g.id].another_group.player1.first_name} and {games[g.id].another_group.player2.first_name}     ...............     {games[g.id].another_group.group_score()}\n\n{display} it`s your trun. Play your card."
            playing = playing_shelem(games[g.id].players, games[g.id].ruler, games[g.id].ruler_group, games[g.id].another_group, games[g.id].rule_sign, games[g.id].answer[games[g.id].players[0].user_id], games[g.id].answer[games[g.id].players[1].user_id], games[g.id].answer[games[g.id].players[2].user_id], games[g.id].answer[games[g.id].players[3].user_id])
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= text_playing, reply_markup= playing, parse_mode="HTML")
            bot.answer_callback_query(call.id)

        elif call.from_user.id == games[g.id].turn:
            print("\n\n\n\n33333333333333333\n\n\n\n")
            print(games[g.id].played_cards)
            print(games[g.id].current_rule)
            card_num = card_number(call.data, call.from_user.id, games[g.id].players)
            is_played = True
            if len(games[g.id].played_cards) == 0:
                games[g.id].current_rule = set_current_rule(call.data, call.from_user.id, games[g.id].players)
                games[g.id].played_cards[card_num] = call.from_user.id
                games[g.id].answer[games[g.id].turn] = cards[card_num]
                games[g.id].turn = next_turn(games[g.id].turn, games[g.id].players)
            elif card_num not in games[g.id].current_rule and have_current_rule(games[g.id].current_rule, games[g.id].turn, games[g.id].players):
                bot.answer_callback_query(call.id, "You can`t play this card. Choose another one!")
                is_played = False

            elif len(games[g.id].played_cards) == 3:
                print("\n\n\n\n89898989989898989898989898989\n\n\n\n")
                games[g.id].played_cards[card_num] = call.from_user.id
                print(games[g.id].ruler_group.cards)
                print(games[g.id].another_group.cards)
                games[g.id].answer[games[g.id].turn] = cards[card_num]
                games[g.id].turn = set_score(games[g.id].played_cards, games[g.id].rule, games[g.id].ruler_group, games[g.id].another_group, games[g.id].players, games[g.id].current_rule)
                text_playing2 = f"Shelem game\n\n{games[g.id].ruler_group.color}:{games[g.id].ruler_group.player1.first_name} and {games[g.id].ruler_group.player2.first_name}     ...............     {games[g.id].ruler_group.group_score()}/{games[g.id].final_score}\n{games[g.id].another_group.color}:{games[g.id].another_group.player1.first_name} and {games[g.id].another_group.player2.first_name}     ...............     {games[g.id].another_group.group_score()}\n\n{display} it`s your trun. Play your card."
                playing2 = playing_shelem(games[g.id].players, games[g.id].ruler, games[g.id].ruler_group, games[g.id].another_group, games[g.id].rule_sign, games[g.id].answer[games[g.id].players[0].user_id], games[g.id].answer[games[g.id].players[1].user_id], games[g.id].answer[games[g.id].players[2].user_id], games[g.id].answer[games[g.id].players[3].user_id])
                bot.edit_message_text(inline_message_id=call.inline_message_id, text= text_playing2, reply_markup= playing2, parse_mode="HTML")
                bot.answer_callback_query(call.id)
                sleep(3)
                games[g.id].played_cards.clear()
                games[g.id].answer = {games[g.id].players[0].user_id:" ", games[g.id].players[1].user_id:" ", games[g.id].players[2].user_id:" ", games[g.id].players[3].user_id:" "}
            else:
                games[g.id].played_cards[card_num] = call.from_user.id
                games[g.id].answer[games[g.id].turn] = cards[card_num]
                games[g.id].turn = next_turn(games[g.id].turn, games[g.id].players)
            
            if is_played:
                games[g.id].answer[games[g.id].turn] = "finger"
                for p in games[g.id].players:
                    if p.user_id == games[g.id].turn:
                        display = p.display_name()
                        break
                print(games[g.id].rule, games[g.id].rule_sign)
                text_playing = f"Shelem game\n\n{games[g.id].ruler_group.color}:{games[g.id].ruler_group.player1.first_name} and {games[g.id].ruler_group.player2.first_name}     ...............     {games[g.id].ruler_group.group_score()}/{games[g.id].final_score}\n{games[g.id].another_group.color}:{games[g.id].another_group.player1.first_name} and {games[g.id].another_group.player2.first_name}     ...............     {games[g.id].another_group.group_score()}\n\n{display} it`s your trun. Play your card."
                playing = playing_shelem(games[g.id].players, games[g.id].ruler, games[g.id].ruler_group, games[g.id].another_group, games[g.id].rule_sign, games[g.id].answer[games[g.id].players[0].user_id], games[g.id].answer[games[g.id].players[1].user_id], games[g.id].answer[games[g.id].players[2].user_id], games[g.id].answer[games[g.id].players[3].user_id])
                bot.edit_message_text(inline_message_id=call.inline_message_id, text= text_playing, reply_markup= playing, parse_mode="HTML")
                bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, "it`s not your turn")
        
        if len(games[g.id].ruler.cards) == 0:
            end_text = set_winner(games[g.id].ruler_group, games[g.id].another_group, games[g.id].final_score)
            end = end_game()
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= end_text, reply_markup= end)
            bot.answer_callback_query(call.id)
            del g
   




    @bot.callback_query_handler(func= lambda call: call.data == "myhand")
    def my_hand(call):
        watch_hand(call.from_user.id, call.id, games[g.id].players, cards)
    
    @bot.callback_query_handler(func= lambda call: call.data == "myhand_2")
    def my_hand2(call):
        if call.from_user.id == games[g.id].ruler.user_id:
            watch_ruler_hand(call.from_user.id, call.id, games[g.id].players, cards, games[g.id].ruler_group)
        else:
            watch_hand(call.from_user.id, call.id, games[g.id].players, cards)

    @bot.callback_query_handler(func= lambda call: call.data in["p1","c1","c2","p2","p3","c3","c4","p4","ruler","rule","group1_3","group2_3"])
    def doesnt_work(call):
        bot.answer_callback_query(call.id, "this button doesn`t work")
    
    
    @bot.callback_query_handler(func= lambda call: call.data.startswith("forward_to_"))
    def forward(call):
        chat_id = int(call.data.split("_")[2])
        # Forward the message to the selected group
        bot.forward_message(chat_id, call.message.chat.id, call.message.message_id)


    @bot.message_handler(func=lambda msg: True)
    def echo_all():
        pass

    bot.infinity_polling()






@bot.message_handler(commands=["greet"])
def greet(messege):
    first_name = messege.from_user.first_name
    user_id = messege.from_user.id
    message_text = f"Click <a href='tg://user?id={user_id}'>{first_name}</a> to view Anna's profile."
    bot.send_message(chat_id=messege.chat.id, text=message_text, parse_mode="HTML")



def start():
    mark_start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    mark_start.add("play with friends", "support")

    @bot.message_handler(commands=["start"])
    def greet(messege):
        bot.send_message(messege.chat.id, """
Hey, wellcome to Shelem Bot
this bot is provided to play the most intresting card game, SHELEM.
if you dont know how to play shelem at all, visit this link:
https://fa.wikipedia.org/wiki/%D8%B4%D9%84%D9%85_(%D8%A8%D8%A7%D8%B2%DB%8C)

or for english reference visit this one:
https://en.wikipedia.org/wiki/Shelem#:~:text=Rules,-Card%2Dpoint%20values&text=Each%20player%20receives%2012%20cards,the%20widow%20and%20making%20trumps.
""", reply_markup=mark_start)


def deal_cards(card_numbers, players):
    for _ in range(12):
        for player in players:
            number = random.choice(card_numbers)
            card_numbers.remove(number)
            player.cards.append(number)

    for i in players:
        i.cards.sort()
        print(i.cards)

def make_groups(players):
    list1 = []
    list2 = []
    for i in range(2):
        p = random.choice(players)
        list1.append(p)
        players.remove(p)
    list2 = players.copy()
    players.clear()
    players.append(list1[0])
    players.append(list2[0])
    players.append(list1[1])
    players.append(list2[1])
    return list1, list2


def lets_play():
    keyboard_lets_play = types.InlineKeyboardMarkup(row_width=2)
    button_iam_in = types.InlineKeyboardButton(text="I am in", callback_data="join_game")
    button_start = types.InlineKeyboardButton(text="start the game", callback_data="start_game")
    keyboard_lets_play.add(button_iam_in, button_start)
    return keyboard_lets_play


def calling_score(players, p_score, p1_s=" ", p2_s=" ", p3_s =" ", p4_s=" "):
    responses = [p1_s, p2_s, p3_s, p4_s]
    for i in range(4):
        if responses[i] == "finger" and (i == 0 or i == 3):
            responses[i] = "👈"
        elif responses[i] == "finger" and (i == 1 or i == 2):
            responses[i] = "👉"

    calling = types.InlineKeyboardMarkup(row_width=5)
    p1_1 = types.InlineKeyboardButton(text= players[0].first_name, callback_data="p1")
    c1_1 = types.InlineKeyboardButton(text=responses[0], callback_data="c1")
    c2_1 = types.InlineKeyboardButton(text=responses[1], callback_data="c2")
    p2_1 = types.InlineKeyboardButton(text= players[1].first_name, callback_data="p2")
    calling.row(p1_1, c1_1, c2_1, p2_1)
    p4_1 = types.InlineKeyboardButton(text= players[3].first_name, callback_data="p4")
    c4_1 = types.InlineKeyboardButton(text=responses[3], callback_data="c4")
    c3_1 = types.InlineKeyboardButton(text=responses[2], callback_data="c3")
    p3_1 = types.InlineKeyboardButton(text= players[2].first_name, callback_data="p3")
    calling.row(p4_1, c4_1, c3_1, p3_1)
    my_hand_1 = types.InlineKeyboardButton(text= "my hand", callback_data="myhand")
    ruler_1 = types.InlineKeyboardButton(text= "ruler: ?", callback_data="ruler")
    rule_1 = types.InlineKeyboardButton(text= "rule: ?", callback_data="rule")
    calling.row(my_hand_1, ruler_1, rule_1)
    scores1_1 = [types.InlineKeyboardButton(f"{i}", callback_data=f"score1_{i}") for i in range(int(p_score) + 5, 166, 5)]
    calling.add(*scores1_1)
    pass_1 = types.InlineKeyboardButton(text= "pass", callback_data="pass_1")
    calling.row(pass_1)
    return calling


def make_rule_button(players, ruler, p1_s=" ", p2_s=" ", p3_s =" ", p4_s=" "):
    numbers = ["⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "❿", "⓫", "⓬", "⓭", "⓮", "⓯", "⓰", "⓱", "⓲", "⓳", "⓴"]
    responses = [p1_s, p2_s, p3_s, p4_s]
    for i in range(4):
        if responses[i] == "finger" and (i == 0 or i == 3):
            responses[i] = "👈"
        elif responses[i] == "finger" and (i == 1 or i == 2):
            responses[i] = "👉"

    ruling = types.InlineKeyboardMarkup(row_width=5)
    p1_2 = types.InlineKeyboardButton(text= players[0].first_name, callback_data="p1")
    c1_2 = types.InlineKeyboardButton(text=responses[0], callback_data="c1")
    c2_2 = types.InlineKeyboardButton(text=responses[1], callback_data="c2")
    p2_2 = types.InlineKeyboardButton(text= players[1].first_name, callback_data="p2")
    ruling.row(p1_2, c1_2, c2_2, p2_2)
    p4_2 = types.InlineKeyboardButton(text= players[3].first_name, callback_data="p4")
    c4_2 = types.InlineKeyboardButton(text=responses[3], callback_data="c4")
    c3_2 = types.InlineKeyboardButton(text=responses[2], callback_data="c3")
    p3_2 = types.InlineKeyboardButton(text= players[2].first_name, callback_data="p3")
    ruling.row(p4_2, c4_2, c3_2, p3_2)
    my_hand_2 = types.InlineKeyboardButton(text= "my hand", callback_data="myhand_2")
    ruler_2 = types.InlineKeyboardButton(text= f"ruler: {ruler.first_name}", callback_data="ruler")
    rule_2 = types.InlineKeyboardButton(text= "rule: ?", callback_data="rule")
    ruling.row(my_hand_2, ruler_2, rule_2)
    cart1 = [types.InlineKeyboardButton(f"{numbers[i]}", callback_data=f"cart1_{i}") for i in range(1, 17)]
    ruling.add(*cart1)  
    return ruling


def playing_shelem(players, ruler, ruler_group, another_group, rule=" ?", p1_s=" ", p2_s=" ", p3_s =" ", p4_s=" "):
    numbers = ["⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "❿", "⓫", "⓬", "⓭", "⓮", "⓯", "⓰", "⓱", "⓲", "⓳", "⓴"]
    responses = [p1_s, p2_s, p3_s, p4_s]
    for i in range(4):
        if responses[i] == "finger" and (i == 0 or i == 3):
            responses[i] = "👈"
        elif responses[i] == "finger" and (i == 1 or i == 2):
            responses[i] = "👉"

    all_round = ruler_group.win_round + another_group.win_round
    playing = types.InlineKeyboardMarkup(row_width=5)
    p1_3 = types.InlineKeyboardButton(text= players[0].first_name, callback_data="p1")
    c1_3 = types.InlineKeyboardButton(text=responses[0], callback_data="c1")
    c2_3 = types.InlineKeyboardButton(text=responses[1], callback_data="c2")
    p2_3 = types.InlineKeyboardButton(text= players[1].first_name, callback_data="p2")
    playing.row(p1_3, c1_3, c2_3, p2_3)
    p4_3 = types.InlineKeyboardButton(text= players[3].first_name, callback_data="p4")
    c4_3 = types.InlineKeyboardButton(text=responses[3], callback_data="c4")
    c3_3 = types.InlineKeyboardButton(text=responses[2], callback_data="c3")
    p3_3 = types.InlineKeyboardButton(text= players[2].first_name, callback_data="p3")
    playing.row(p4_3, c4_3, c3_3, p3_3)
    my_hand_3 = types.InlineKeyboardButton(text= "my hand", callback_data="myhand")
    ruler_3 = types.InlineKeyboardButton(text= f"ruler: {ruler.first_name}", callback_data="ruler")
    rule_3 = types.InlineKeyboardButton(text= rule, callback_data="rule")
    playing.row(my_hand_3, ruler_3, rule_3)
    group1_3 = types.InlineKeyboardButton(text= f"{ruler_group.color} team: {ruler_group.win_round}", callback_data="group1_3")
    group2_3 = types.InlineKeyboardButton(text= f"{another_group.color} team: {another_group.win_round}", callback_data="group2_3")
    playing.row(group1_3, group2_3)
    cart3 = [types.InlineKeyboardButton(f"{numbers[i]}", callback_data=f"cart3_{i}") for i in range(1, (14 - all_round))]
    playing.add(*cart3)
    return playing


def end_game():
    end = types.InlineKeyboardMarkup(row_width=2)
    rematch = types.InlineKeyboardButton(text= "🔄️rematch", switch_inline_query_current_chat="")
    friends = types.InlineKeyboardButton(text= "👥with friends", switch_inline_query="")
    end.add(rematch, friends)
    return end


def watch_hand(userid, callid, players, cards):
    numbers = ["❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "❿", "⓫", "⓬", "⓭", "⓮", "⓯", "⓰", "⓱", "⓲", "⓳", "⓴"]
    text = "\n"
    for player in players:
        if userid == player.user_id:
            x = len(player.cards)
            for i in range(x):
                text += f"{numbers[i]}{cards[player.cards[i]]} "
                if (i+1) % 5 == 0:
                    text += "\n"
            bot.answer_callback_query(callid, text, show_alert=True)
            break

    bot.answer_callback_query(callid, "you are not joined in this game")




def watch_ruler_hand(userid, callid, players, cards, ruler_group):
    for player in players:
        if userid == player.user_id:
            bot.answer_callback_query(callid, f"""
❶{cards[player.cards[0]]} ❷{cards[player.cards[1]]} ❸{cards[player.cards[2]]} ❹{cards[player.cards[3]]} ❺{cards[player.cards[4]]}
❻{cards[player.cards[5]]} ❼{cards[player.cards[6]]} ❽{cards[player.cards[7]]} ❾{cards[player.cards[8]]} ❿{cards[player.cards[9]]}
⓫{cards[player.cards[10]]} ⓬{cards[player.cards[11]]}
.................................................................
⓭{cards[player.cards[12]]} ⓮{cards[player.cards[13]]} ⓯{cards[player.cards[14]]} ⓰{cards[player.cards[15]]}
            """, show_alert=True)
            break

    bot.answer_callback_query(callid, "you are not joined in this game")

def dump_cards(ruler, calldata, callid, ruler_group):
    number = ruler.cards[int(calldata[6:]) - 1]
    if number in ruler_group.cards:
        bot.answer_callback_query(callid, "you already dump this card! choos another one")
    else:
        ruler_group.cards.append(number)
    
def set_rule(caldata, player):
    number = player.cards[int(caldata[6:]) - 1]
    list1 = [((number-1)//13)*13 + x for x in range(1, 14)]
    sign = cards[list1[1]][1]
    return list1, sign

def next_turn(turnn, players):
    turn_ind = 0
    for player in players:
        if player.user_id == turnn:
            turn_ind = players.index(player)
    
    return players[(turn_ind + 1) % 4].user_id

def set_current_rule(caldata, userid, players):
    for player in players:
        if player.user_id == userid:
            number = player.cards[int(caldata[6:]) - 1]
            list1 = [((number-1)//13)*13 + x for x in range(1, 14)]
            return list1

def card_number(caldata, userid, players):
    for player in players:
        if player.user_id == userid:
            return player.cards[int(caldata[6:]) - 1]



def set_score(played_cards, rule, group11, group22, players, current_rule):
    played = []
    heads = []
    for item in played_cards.keys():
        played.append(item)
    
    for card in played:
        if card in rule:
            heads.append(card)
    
    if len(heads) == 0:
        for cardd in played:
            if cardd in current_rule:
                heads.append(cardd)

    if played_cards[min(heads)] in group11.player_ids:
        group11.cards.extend(played)
    else:
        group22.cards.extend(played)
    
    for player in players:
        for cd in played:
            if player.user_id == played_cards[cd]:
                player.cards.remove(cd)

    return played_cards[min(heads)]

def have_current_rule(cur_rule: list, userid, players):
    current_player = None
    for player in players:
        if player.user_id == userid:
            current_player = player
    
    for card in current_player.cards:
        if card in cur_rule:
            return True
    return False

def set_winner(ruler_group11: Group, group22: Group, f_score):
    if ruler_group11.group_score() >= f_score:
        c = ruler_group11.color
        return f"Shelem game\n\n{ruler_group11.color}:{ruler_group11.player1.first_name} and {ruler_group11.player2.first_name}     ...............     {ruler_group11.group_score()}/{f_score}\n{group22.color}:{group22.player1.first_name} and {group22.player2.first_name}     ...............     {group22.group_score()}\n\n{ruler_group11.color_team} gets {ruler_group11.group_score()} score and called {f_score}\n{group22.color_team} gets {group22.group_score()} score\n\n{c}{c}{c}{c}{c}{ruler_group11.color_team} wins{c}{c}{c}{c}{c}"
    
    c = group22.color
    return f"Shelem game\n\n{ruler_group11.color}:{ruler_group11.player1.first_name} and {ruler_group11.player2.first_name}     ...............     -{ruler_group11.group_score()}/{f_score}\n{group22.color}:{group22.player1.first_name} and {group22.player2.first_name}     ...............     {group22.group_score()}\n\n{ruler_group11.color_team} gets {ruler_group11.group_score()} score and called {f_score}\n{group22.color_team} gets {group22.group_score()} score\n\n{c}{c}{c}{c}{c}{group22.color_team} wins{c}{c}{c}{c}{c}"




if __name__ == "__main__":
    main()