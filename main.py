from parser import Parser

if __name__ == "__main__":
    p = Parser()
    p.parse_images("https://www.wildberries.ru/catalog/zhenshchinam/odezhda/yubki", "?page=", "dataset")
