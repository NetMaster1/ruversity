from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subject/<int:subject_id>', views.subject, name='subject'),
    path('gen_search/', views.gen_search, name='gen_search'),
    path('sorting/<int:category_id>', views.sorting, name='sorting'),
    path('main_page/', views.main_page, name='main_page'),
    path('list_software/', views.list_software, name='list_software'),
    path('list_fitness/', views.list_fitness, name='list_fitness'),
    path('list_skills/', views.list_skills, name='list_skills'),
    path('list_arts/', views.list_arts, name='list_arts'),
    path('list_buisness/', views.list_buisness, name='list_buisness'),
    path('list_personal/', views.list_personal, name='list_personal'),
    path('list_fundamental/', views.list_fundamental, name='list_fundamental'),
    path('list_languages/', views.list_languages, name='list_languages'),
    path('search_by_author/<int:subject_author>', views.search_by_author, name='search_by_author'),
    path('create_cart_item/<int:subject_id>', views.create_cart_item, name='create_cart_item'),
    path('cart/', views.cart, name='cart'),
    path('delete_from_cart/<int:subject_id>', views.delete_from_cart, name='delete_from_cart'),
    # path('detailed_search/', views.detailed_search, name='detailed_search'),
]
