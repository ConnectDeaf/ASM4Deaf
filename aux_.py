import os

def save_gif_on_the_file_system(request, filepath_root, filename):

    filepath = f"{filepath_root}{filename}"
    request.files.get("GIFfile").save(filepath)

    return filepath


def delete_gif_file_from_file_system(filepath):
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    
    return False


def prepare_database_keyword_query(sign_language, keywords):

    query_str = f"SELECT * FROM videos WHERE LanguageID={sign_language}"

    for kword in keywords:
        query_str += f" AND Keywords LIKE '%{kword}%'"

    return query_str


def create_dictionary_array_from_cursor_results(cursor_results):
    
    result_dictionary = []
    
    for row in cursor_results:
        gif_record_dict = row._asdict()
        result_dictionary.append({
            "id" : gif_record_dict["VideoID"],
            "filename": gif_record_dict["FileName"]
        })
    
    return result_dictionary

