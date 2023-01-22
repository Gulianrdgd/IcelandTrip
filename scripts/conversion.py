import os
import sys


def convert_files(root, file):
    print("Adding file header to: " + file)
    print(root)
    header = "--- \n" \
             "layout: page\n" \
             "title: {file} \n" \
             "categories: [{category}] \n" \
             "---\n".format(file=file[:-3], category=root.split("/")[-1])

    print(header)

    with open(os.path.join(root, file), "r+") as f:
        content = f.read()

        # Fix images
        content = content.replace("Tour|", "")

        # Fix links to other websites
        content_lines = content.splitlines()
        for line in content_lines:
            if "https://" in line[0:9] and not ".jpg" in line and not ".png" in line and not ".jpeg" in line:
                print(line)
                content = content.replace(line, "[" + line + "](" + line + ")")
            else:
                start = line.find("[[")
                end = line.find("]]")
                if start != -1 and end != -1:
                    link = line[start + 2:end]
                    content = content.replace(line, "[" + link + "]({% link Interesting places/" + link + ".md %})")
        f.seek(0, 0)

        # Append header
        f.write(header + content)


def navigate_folder_structure(path):
    print("Indexing folder structure: " + path)
    structure = []
    done = False
    while not done:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".md"):
                    convert_files(root, file)
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