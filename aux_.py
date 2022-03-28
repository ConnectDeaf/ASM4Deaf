def save_gif_on_the_file_system(request, filepath_root):

    filename = request.files.get("GIFfile").filename
    filepath = filepath_root + filename
    request.files.get("GIFfile").save(filepath)

    return filepath
    