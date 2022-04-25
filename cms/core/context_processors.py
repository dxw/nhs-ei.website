def request_contexts(request):
    return {
        "request_url": request.build_absolute_uri(request.path)
    }