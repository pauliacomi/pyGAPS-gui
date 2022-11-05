import pathlib


def _get_res_dir():
    """Convenience get resource directory"""
    return pathlib.Path(__file__).parent.parent / 'resources'


def get_resource(path_or_file):
    """Convenience function to locate resources."""
    return str(_get_res_dir() / path_or_file)


def get_resource_content(path, glob="*.*"):
    """Convenience function to locate an entire folder of resources."""
    return tuple((_get_res_dir() / path).glob(glob))
