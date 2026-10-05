import aiohttp
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.last_feed_time = datetime.now()
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.img = None
        self.name = None
        self.hp = random.randit(200,400)
        self.power = random.randit(30,60)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Pokémonunuzun ismi: {self.name} Pokemonun Gücü: {self.power} Pokemonun Canı: {self.hp}"
    
    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
    async def feed(self, feed_interval= 20, hp_increase=10 ):
        current_time = datetime.now() 
        delta_time = timedelta(seconds=feed_interval) 
        if (current_time - self.last_feed_time) > delta_time :
            self.hp += hp_increase
            self.last_feed_time = current_time 
            return f"Pokémon sağlığı geri yüklenir. Mevcut HP: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz:{self.last_feed_time + delta_time }"
    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açmak
            async with session.get(url) as response:  # Pokémon verilerini almak için bir GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması
                    img_url = data['sprites']['front_default']  #  Pokémonun URL'sini alma
                    return img_url  # Resmin URL'sini döndürme
                else:
                    return Pikachu  # İstek başarısız olursa None döndürür

class Fighter(Pokemon):
    async def feed(self):
        return super().feed(hp_increase=20)
    async def attack(self,enemy):
        super_power = random.randit(5,15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDövüşçü Pokemon süper saldırı kullandı. Eklenen güç: {super_power}"



class Knight(Pokemon):
    async def attack(self,enemy):
        magical_sword = random.randit(10,20)
        self.power += magical_sword
        result = await super().attack(enemy)
        self.power -= magical_sword
        return result + f"\nDövüşçü Pokemon büyülü kılıç kullandı. Eklenen güç: {magical_sword}"

if __name__ == "__main__":
import asyncio

async def main():
        # Test için iki Pokémon oluşturma
        trainer1 = "Ash"
        trainer2 = "Misty"
        pokemon1 = Pokemon(trainer1)
        pokemon2 = Pokemon(trainer2)

        # Pokémon adlarını ve bilgilerini yazdırma
        print(trainer1, "Pokémonu:", await pokemon1.get_name())
        print(await pokemon1.info())
        print(trainer2, "Pokémonu:", await pokemon2.get_name())
        print(await pokemon2.info())

        # Pokémonlar arasında saldırı simülasyonu
        print(await pokemon1.attack(pokemon2))
        print(await pokemon2.attack(pokemon1))
        

    asyncio.run(main())