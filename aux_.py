import os
from unittest import result

def save_gif_on_the_file_system(request, filepath_root, filename):

    filepath = f"{filepath_root}{filename}"
    request.files.get("GIFfile").save(filepath)

    return filepath


def delete_gif_file_from_file_system(filepath):
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    
    return False


def prepare_database_keyword_query(sign_language, gif_type, keywords):

    query_str = "SELECT * FROM "

    if gif_type == 'h' or gif_type == 'b':
        query_str += f"bodyparts WHERE PartType='{gif_type}' AND"
    else:
        query_str += "fullbodys WHERE"


    query_str += f" LanguageID={sign_language}"

    for kword in keywords:
        query_str += f" AND Keywords LIKE '%{kword}%'"

    return query_str


def create_ids_dictionary_from_cursor_results(cursor_results):
    
    result_dictionary = {"ids" : []}
    
    for row in cursor_results:
        result_dictionary["ids"].append(row._asdict()["BodyPartID"])
    
    return result_dictionary