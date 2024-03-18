def create_execute_string(fl: str, file_location: str, file_type: str):
    execute_string = "java -jar " + file_location + " xz " + fl + file_type
    return execute_string
