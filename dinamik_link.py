import json

# Load the JSON data

# Category to URL parameter mapping
category_to_param = {
    "Also speaks": "tl",
    "Daytime": "time",
    "Sort by": "sort",
    "Specialties": "tags",
    "Region accent": "tags",  # Assuming this should be part of 'tags'
    "Test preparation": "tags",  # Assuming this should be part of 'tags'
    "Learning disabilities": "tags",  # Assuming this should be part of 'tags'
    "Only professional tutors": "additional",
    "Only English native speakers": "additional",
    "Only super tutors": "additional",
    "Days": "day",
    "Country": "CoB"
}

# Function to process user input
def process_input(user_input, available_options):
    if not user_input:  # Check if the input is empty
        return ''
    choices = [choice.strip() for choice in user_input.split(',')]
    valid_choices = [available_options.get(choice, '') for choice in choices if choice in available_options]
    return '%2C'.join(filter(None, valid_choices))  # Join with URL-encoded comma


def collect_inputs(data):
    user_inputs = {}
    for category, options in data.items():
        # Показываем все доступные варианты для каждой категории
        print(f"\n{category}:")
        for i, option in enumerate(options.keys(), start=1):
            print(f"{i}. {option}")

        # Просим пользователя ввести номера выбранных вариантов через запятую
        user_input_numbers = input(
            "Enter the numbers of the options you want to select, separated by commas (e.g., 1,3,4) or skip by pressing enter: ")

        # Обрабатываем ввод пользователя
        if user_input_numbers.strip():
            selected_numbers = [int(num.strip()) for num in user_input_numbers.split(",") if num.strip().isdigit()]
            selected_options = [list(options.keys())[num - 1] for num in selected_numbers if 0 < num <= len(options)]
            user_inputs[category] = ', '.join(selected_options)
        else:
            user_inputs[category] = ''

    return user_inputs


def construct_url(base_url, category_to_param, data, user_inputs):
    query_string_parts = []
    additional_parts = []  # Список для 'additional' параметров и их специальных значений

    # Сначала обрабатываем все параметры, кроме 'additional', 'day', и 'CoB'
    for category, param in category_to_param.items():
        if category in user_inputs and category not in ['Days', 'Country']:
            input_value = user_inputs[category]
            options = data.get(category, {})
            params = process_input(input_value, options)
            if params and 'additional' not in param:
                query_string_parts.append(f"{param}={params}")

    # Формируем строку для 'additional' параметров
    additional_selected = []
    if "Only professional tutors" in user_inputs:
        additional_selected.append("certified")
    if "Only English native speakers" in user_inputs:
        additional_selected.append("native")
    if "Only super tutors" in user_inputs:
        additional_selected.append("only_super_tutors")


    # Если есть выбранные 'additional' параметры, формируем их строку
    if additional_selected:
        # Добавляем первый параметр с префиксом 'additional='
        additional_parts.append(f"additional=additional%3D{additional_selected[0]}")
        # Добавляем остальные параметры без повторения префикса 'additional='
        for param in additional_selected[1:]:
            additional_parts.append(f"additional%3D{param}")
        # Добавляем каждый 'additional' параметр еще раз без префикса для дублирования
        additional_parts.extend([f"{param}" for param in additional_selected])

    # Добавляем сформированные 'additional' параметры
    if additional_parts:
        query_string_parts.append("%2C".join(additional_parts))

    # Обрабатываем 'day' и 'CoB'
    for end_param in ['Days', 'Country']:
        if end_param in user_inputs:
            param = category_to_param[end_param]
            value = process_input(user_inputs[end_param], data[end_param])
            if value:
                query_string_parts.append(f"{param}={value}")

    # Собираем итоговый URL
    constructed_url = f"{base_url}?{'&'.join(query_string_parts)}"
    return constructed_url


base_url = "https://preply.com/en/online/english-tutors"

with open('data.json', 'r') as file:
    data = json.load(file)

if __name__ == '__main__':
    user_inputs = collect_inputs(data)
    dynamic_url = construct_url(base_url, category_to_param, data, user_inputs)
    print("Constructed URL:", dynamic_url)
