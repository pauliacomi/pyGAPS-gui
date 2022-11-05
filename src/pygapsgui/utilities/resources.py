import pathlib


# Resources
def get_resource(path_or_file):
    """Convenience function to locate resources."""
    return str(pathlib.Path(__file__).parent.parent / 'resources' / path_or_file)
