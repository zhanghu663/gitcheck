from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^serial/config/$', views.get_serial_config),  # 获取串口的配置信息
    url(r'^printer/connect/$', views.get_connect), # 创建serial对象
    url(r'^printer/status/$', views.change_printer_status),  # 打印状态的改变
    url(r'^test/$', views.test),  # http测试
    url(r'^printer/$', views.test2_websocket), # ws测试
]