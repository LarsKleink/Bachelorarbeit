def create_execute_string(fl: str, program_location: str, file_type: str):
    execute_string = ("cargo +nightly run --manifest-path " + program_location +
                      "/Cargo.toml --release  --package buff --bin comp_profiler " +
                      fl + file_type + " buff 10000 1.1509")
    return execute_string

