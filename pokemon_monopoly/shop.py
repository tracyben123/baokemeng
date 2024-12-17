class Shop:
    def __init__(self):
        self.items = {
            'pokeball': {'price': 100, 'desc': '用于捕获宝可梦'},
            'potion': {'price': 50, 'desc': '恢复宝可梦HP'},
            'evolution_stone': {'price': 300, 'desc': '用于进化宝可梦'}
        }
        
    def buy_item(self, player, item_name):
        """购买道具"""
        if item_name in self.items:
            item = self.items[item_name]
            if player.money >= item['price']:
                player.money -= item['price']
                player.items[item_name] = player.items.get(item_name, 0) + 1
                return True
        return False
        
    def sell_item(self, player, item_name):
        """出售道具"""
        if item_name in player.items and player.items[item_name] > 0:
            sell_price = self.items[item_name]['price'] // 2
            player.money += sell_price
            player.items[item_name] -= 1
            return True
        return False 