def create_execute_string(file_location: str, program_location: str, file_type: str):
    execute_string = "java -jar " + program_location + " chimp " + file_location + file_type
    return execute_string
