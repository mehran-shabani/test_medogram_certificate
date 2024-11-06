def binary_generator():
    file_path = 'logo.png'
    with open(file_path, "rb") as image_file:
        binary_data = image_file.read()
    return binary_data


