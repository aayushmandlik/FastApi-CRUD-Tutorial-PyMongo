def blogEntity(item) -> dict:
    return {
        "id":str(item['_id']),
        "title":item["title"],
        "body": item["body"]
    }

def blogsEntity(entity) -> list:
    return [blogEntity(item) for item in entity ]