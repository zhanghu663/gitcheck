from django.urls import path, include

urlpatterns = [
    path("cxsw/", include("printer_center.urls")),
    path("test/", include("test_printer.urls")),
]
