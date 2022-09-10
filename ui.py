from tkinter import *
import scraper as scraper
URL = "https://www.mtggoldfish.com/deck_searches/create?utf8=%E2%9C%93&deck_search%5Bname%5D=&deck_search%5Bformat%5D=&deck_search%5Btypes%5D%5B%5D=&deck_search%5Btypes%5D%5B%5D=tournament&deck_search%5Btypes%5D%5B%5D=user&deck_search%5Bplayer%5D=&deck_search%5Bdate_range%5D=08%2F27%2F2022+-+09%2F10%2F2022&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=Temporary+Lockdown&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter=2&commit=Search"

def call_decks():
    scraper.get_decks(URL)

def start_builder():
    window = Tk()
    window.title("MTG Deck Builder")
    window.config(padx=50, pady=50)

    canvas = Canvas(width=300, height=414)
    background_img = PhotoImage(file="UI/background.png")
    canvas.create_image(150, 207, image=background_img)
    quote_text = canvas.create_text(150, 207, text="Kanye Quote Goes HERE", width=250, font=("Arial", 30, "bold"), fill="white")
    canvas.grid(row=0, column=0)

    kanye_img = PhotoImage(file="UI/kanye.png")
    kanye_button = Button(image=kanye_img, highlightthickness=0, command=call_decks)
    kanye_button.grid(row=1, column=0)



    window.mainloop()
