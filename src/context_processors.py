import json

def search_history(request):
    search_history_json = json.dumps(request.session.get('search_history', []))
    return {'search_history_json': search_history_json}