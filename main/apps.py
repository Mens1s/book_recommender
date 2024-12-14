from django.apps import AppConfig
from .utils.ai import AI


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        AI.createRecommendationInstance()
        AI.getMostPopularBooksByCategories()  
