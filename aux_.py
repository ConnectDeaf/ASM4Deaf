import os


def save_on_the_file_system(request, filename_getter_name , filepath_root, filename):

    filepath = f"{filepath_root}{filename}"
    request.files.get(filename_getter_name).save(filepath)

    return filepath


def delete_file_from_file_system(filepath):
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    
    return False


def prepare_database_keyword_query(hand, keywords):

    query_str = f"SELECT * FROM videos WHERE hand='{hand}'"

    for kword in keywords:
        query_str += f" AND keywords='{kword}'"

    return query_str


def create_dictionary_array_from_cursor_results(cursor_results):
    
    result_dictionary = []
    
    for row in cursor_results:
        gif_record_dict = row._asdict()
        result_dictionary.append({
            "id" : gif_record_dict["id"],
            "username": gif_record_dict["username"],
            "keywords": gif_record_dict["keywords"],
            "title": gif_record_dict["title"],
            "target_file": gif_record_dict["target_file"],
            "download_file": gif_record_dict["download_file"],
            "subtitles": gif_record_dict["subtitles"],
            "country": gif_record_dict["country"],
            "race": gif_record_dict["race"],
            "gender": gif_record_dict["gender"],
            "hand": gif_record_dict["hand"]
        })
    
    return result_dictionary




