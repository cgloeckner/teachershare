import pathlib
import shutil


def get_dirs_inside(dir: pathlib.Path) -> list:
    """Return list of pathobjects inside `dir` that are directories themselves."""
    return sorted([item for item in dir.iterdir() if item.is_dir()])


def get_students(dir: pathlib.Path) -> dict:
    """Return dict that maps class names to lists of pathobjects that point to student dirs."""
    all_classes = get_dirs_inside(dir)
    return {c.name: get_dirs_inside(c) for c in all_classes}


def copy_element(src_path: pathlib.Path, dst_dir: pathlib.Path) -> None:
    """Copy the given source path (file or dir) into a given destination dir."""
    assert(dst_dir.is_dir())
    dst_dir /= src_path.name
    
    if src_path.is_dir():
        shutil.copytree(src_path, dst_dir)
    else:
        shutil.copyfile(src_path, dst_dir)
