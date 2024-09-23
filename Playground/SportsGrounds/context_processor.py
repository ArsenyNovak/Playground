
navigation = [{'name': "Главная страница", 'url_name': 'home'},
              {'name': "О сайте", 'url_name': 'about'},
              {'name': "Все площадки", 'url_name': 'all_playgrounds'},
              {'name': "Добавить площадку", 'url_name': 'add_playground'},
              {'name': "Обратная связь", 'url_name': 'contact'},
             ]

def get_navigation(request):
    return {'navigation': navigation}