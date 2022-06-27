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


def prepare_database_keyword_query(sign_language, keywords):

    query_str = f"SELECT * FROM videos WHERE LanguageID={sign_language}"

    for kword in keywords:
        query_str += f" AND Keywords LIKE '%{kword}%'"

    return query_str


def create_dictionary_array_from_cursor_results(cursor_results, languages, races):
    
    result_dictionary = []
    languages_dict = {}
    races_dict = {}
    for l in languages:
        languages_dict[l[0]] = l[1]
    for r in races:
        races_dict[r[0]] = r[1]
    
    for row in cursor_results:
        gif_record_dict = row._asdict()
        result_dictionary.append({
            "id" : gif_record_dict["VideoID"],
            "filename": gif_record_dict["FileName"],
            "sign_language": languages_dict[gif_record_dict["LanguageID"]],
            "signer_race": races_dict[gif_record_dict["RaceID"]],
        })
    
    return result_dictionary




