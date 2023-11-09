import sys
import traceback


class HandleExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        print('Error on Load')
        print("Internal Server Error: " + request.get_full_path(), file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        print(exception)
