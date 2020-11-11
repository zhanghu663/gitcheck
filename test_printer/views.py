from http.client import NO_CONTENT

from django.views.decorators.http import require_POST
from test_printer.standard import CxswPrinter


def test(request):
    pass


@require_POST
def create_connection(request):
    command = 'connect'
    cxsw_printer = CxswPrinter()
    cxsw_printer.build_connection(port='COM5', baudrate=115200)
    return NO_CONTENT
