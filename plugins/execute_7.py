def create_execute_string(fl: str, program_location: str, file_type: str):
    execute_string = "java -jar " + program_location + " brotli " + fl + file_type
    return execute_string
