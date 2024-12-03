from bs4 import BeautifulSoup
from msg_split import split_msg

# Загрузить и проанализировать HTML-файл
source_html = input("Введите исходный HTML-каталог:")

if(len(source_html)):
    file_path = source_html 
else:
    file_path = "source.html"
with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()
    
soup = BeautifulSoup(html_content, "html.parser")
soup = BeautifulSoup(soup.prettify(), "html.parser")
root = soup.html or soup.body or soup

# Разделить HTML на части с максимальным ограничением по количеству символов
max_len_char = int(input("Введите максимальную длину каждого фрагмента: "))

if(max_len_char > 0): 
    MAX_LEN = max_len_char
else:
    MAX_LEN = 50

# Распечатать каждую часть
try:
    parts = split_msg(root, MAX_LEN)

    for i, part in enumerate(parts, 1):
        print(f"Фрагмент {i} начинать==============================")
        res_str = ""
        soup = BeautifulSoup(part, "html.parser")
        for content in soup.contents[1:-1]:     
            res_str = res_str + str(content)        
        print(res_str)
        print(f"Фрагмент конец ===================================")
        
except Exception as e:
    print("невозможно выполнить анализ с заданной длиной фрагмента")
        
 