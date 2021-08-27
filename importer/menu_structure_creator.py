import lxml.html

with open("x.html") as f:  # a copy of the header from staging
    html = f.read()
STEP = {
    -1: "], ",
    0: "",
    +1: "[",
}

print("# created by menu_structure_creator.py\nmenu_structure = ", end="")
oldindent = 0
root = lxml.html.fromstring(html)
for a in root.xpath("//a"):
    ancestor = a
    indent = 0
    while ancestor is not None:
        if ancestor.tag == "ul":
            indent = indent + 1
        ancestor = ancestor.getparent()
    diff = indent - oldindent
    name = a.text.strip()
    url = a.attrib["href"]
    if "javascript" in url:
        url = None

    item = repr([name, url]) + ", "
    if name in ["Back", "", "Open mobile menu"]:
        item = ""
    if url and "/publication/" in url and "nhs-england-improvement" not in url:
        item = ""

    print(f"{'    '*indent}{STEP[diff]}{item}", end="")
    oldindent = indent
print("]")

# then run the output through python black
# consider invoking with python3 importer/menu_structure_creator.py > importer/menu_structure.py && black importer/menu_structure.py
