def save_gif_on_the_file_system(request, filepath_root):

    #get filename
    filename = request.files.get("GIFfile").filename
    
    # create the save-location
    filepath = filepath_root + filename
    
    # save the file
    request.files.get("GIFfile").save(filepath)

    return
    