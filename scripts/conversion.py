import os
import sys


def add_file_header(root, file):
    print("Adding file header to: " + file)

    header = "--- \n" \
             "layout: page\n" \
             "title: {file} \n" \
             "---\n".format(file=file[:-3])

    print(header)

    with open(os.path.join(root, file), "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header + content)


def convert_images_to_github_markdown(root, file):
    print("Converting images to github markdown: " + file)

    with open(os.path.join(root, file), "r+") as f:
        content = f.read()
        content = content.replace("Tour|", "")
        f.seek(0, 0)
        f.write(content)


def convert_links_to_hyperlinks(root, file):
    print("Converting links to hyperlinks: " + file)

    with open(os.path.join(root, file), "r+") as f:
        content = f.read()
        content_lines = content.splitlines()
        for line in content_lines:
            if "https://" in line[0:9] and not ".jpg" in line and not ".png" in line and not ".jpeg" in line:
                print(line)
                content = content.replace(line, "[" + line + "](" + line + ")")

        f.seek(0, 0)
        f.write(content)


def convert_md_to_html(root, file):
    print("Converting markdown to html: " + file)

    with open(os.path.join(root, file), "r+") as f:
        content = f.read()
        content = content.replace(".md", ".html")
        f.seek(0, 0)
        f.write(content)


def navigate_folder_structure(path):
    print("Indexing folder structure: " + path)
    structure = []
    done = False
    while not done:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".md"):
                    add_file_header(root, file)
                    convert_images_to_github_markdown(root, file)
                    convert_links_to_hyperlinks(root, file)
                    convert_md_to_html(root, file)
        done = True
    print(structure)
    return structure


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print("Usage: python conversion.py <folder>")
        sys.exit(1)

    folder = args[0]
    print("Converting folder: " + folder)
    navigate_folder_structure(folder)


if __name__ == '__main__':
    main()