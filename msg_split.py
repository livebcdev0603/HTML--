from bs4.element import NavigableString
from bs4 import BeautifulSoup

def split_msg(tag, max_chars):
    """Рекурсивно разбить HTML на части, сохраняя правильную структуру и не нарушая текстовые узлы."""
    parts = []
    current_part = []
    stack = []  
    part_chars = 0
    real_write = False

    def open_tag(tag):
        """Вернуть открывающий тег с атрибутами."""
        if not tag or not tag.name:
            return ""
        attrs = " ".join([f'{k}="{v}"' for k, v in tag.attrs.items()])
        return f"<{tag.name} {attrs.strip()}>" if attrs else f"<{tag.name}>"

    def close_tag(tag):
        """Вернуть закрывающий тег."""
        if not tag or not tag.name:
            return ""
        return f"</{tag.name}>"

    def add_to_part(content):
        """Добавляет содержимое в текущую часть и обновляет количество символов."""
        nonlocal part_chars
        current_part.append(content)
        part_chars += len(content)

    def recursive_split(tag):
        nonlocal part_chars
        nonlocal real_write

        if isinstance(tag, NavigableString):  # Обрабатывать текст напрямую       
            chunk = str(tag)
            if part_chars + len(chunk) + count_tails() > max_chars and current_part:
                finish_part()
            add_to_part(chunk)
            real_write = True
        elif tag.name:  # Обрабатывать только допустимые теги
            add_to_part(open_tag(tag))
            stack.append(tag.name)
            for child in tag.children:
                recursive_split(child)
            stack.pop()
            add_to_part(close_tag(tag))
            
    def count_tails():
        return_val = 0
        if current_part:
            for open_tag_name in reversed(stack):
                return_val = return_val + len(f"</{open_tag_name}>")
        return return_val

    def finish_part():
        """Завершить текущую часть и начать следующую."""
        nonlocal part_chars
        nonlocal real_write
        if real_write is not True:
            raise
        if current_part:
            for open_tag_name in reversed(stack):
                current_part.append(f"</{open_tag_name}>")
            parts.append("".join(current_part))
            current_part.clear()
            part_chars = 0
            for open_tag_name in stack:
                current_part.append(f"<{open_tag_name}>")

    recursive_split(tag)

    if current_part:
        parts.append("".join(current_part))

    return parts
   
def unit_test_parse(file_path, MAX_LEN):
    # Загрузить и проанализировать HTML-файл
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    soup = BeautifulSoup(soup.prettify(), "html.parser")
    root = soup.html or soup.body or soup
    # Распечатать каждую часть
    answer = ""
    try:
        parts = split_msg(root, MAX_LEN)

        for i, part in enumerate(parts, 1):
            answer += f"Фрагмент {i} начинать==============================\n"
            res_str = ""
            soup = BeautifulSoup(part, "html.parser")
            for content in soup.contents[1:-1]:     
                res_str = res_str + str(content)  
            answer += res_str + "\n"
            answer += "Фрагмент конец ===================================\n"
    except Exception as e:
        answer = "невозможно выполнить анализ с заданной длиной фрагмента"

    # with open('answer.html', 'w', encoding="utf-8") as file:
    #     file.write(answer)
    #     file.close()

    return answer