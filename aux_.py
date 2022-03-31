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