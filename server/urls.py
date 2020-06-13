#   This file is part of CentriFi.
#
#   CentriFi is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   CentriFi is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with CentriFi.  If not, see <https://www.gnu.org/licenses/>.
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('api/list-network-info', csrf_exempt(views.list_network_info)),
	path('api/login', csrf_exempt(views.login)),
	path('api/get-wifi-settings', csrf_exempt(views.get_wifi_settings)),
	path('api/set-wifi-settings', csrf_exempt(views.set_wifi_settings)),
	path('api/set-router-passwords', csrf_exempt(views.set_router_passwords)),
	path('api/network-statistics', csrf_exempt(views.network_statistics)),
	path('api/list-end-devices', csrf_exempt(views.list_end_devices)),
	path('api/set-end-devices', csrf_exempt(views.set_end_devices))
]
