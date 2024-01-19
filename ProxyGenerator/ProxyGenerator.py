from Scryfall.Scryfall import Scryfall
from PIL import Image
from io import BytesIO
import os 

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class ProxyGenerator:
    def __init__(self) -> None:
        self.back = Image.open(f'{DIR_PATH}/data/proxy_back.png')

    def generate_proxy(self, card:Image):
        h = 2*card.size[1]
        w = card.size[0]
        im = Image.new("RGBA", (w, h))

        im.paste(card)
        im.paste(self.back.rotate(180).resize((card.size[0], card.size[1])), (0, card.size[1]))

        return im.rotate(-90)
    
    def build_pdf(self, images: [Image]):
        images[0].save("./out.pdf", save_all=True, append_images=images[1:])



def main():
    cards = [
        'lanowar elves', 'elvish mystic', 'quirion ranger', 'staff of domination'
    ]

    scryfall = Scryfall()
    pg = ProxyGenerator()
    
    proxy = []
    
    for card in cards:
        proxy.append(pg.generate_proxy(scryfall.get_image(card)))

    pg.build_pdf(proxy)


if __name__ == "__main__":
    main()