from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add-post$', views.add_post),
    # Parses number from URL and uses it as the item_id argument to the action
    url(r'^delete-post/(?P<post_id>\d+)$', views.delete_post),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login),
    url(r'^register$', views.register),
    url(r'^profile/(?P<username>\w+)$', views.profile),
    url(r'^edit-profile$',views.edit_profile,name='edit_profile'),
    url(r'^photo/(?P<username>\w+)$',views.get_photo, name='photo'),
]
