import os
from argparse import ArgumentParser
from pymupdf import Document

parser: ArgumentParser = ArgumentParser("split-pdf")
parser.add_argument(
    "filename",
    type = str,
    help = "The file to be split."
)
parser.add_argument(
    "-o", "--output-directory",
    type = str,
    default = "./",
    help = "The output directory for the PDF files."
)
parser.add_argument(
    "-s", "--separator",
    type = str,
    default = " - ",
    help = "The separator used to separate level names."
)
parser.add_argument(
    "-l", "--depth",
    type = int,
    default = "1",
    help = "The level the document should be parsed to."
)

arguments = parser.parse_args()

def Split(fileName: str,
          outputDir: str,
          separator: str,
          depth: int) -> None:
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)

    input: Document = Document(fileName)
    inputData = input.tobytes()

    outline: list[tuple[int, str, int]] = input.get_toc() # type: ignore
    outline.sort(key = lambda x: x[2])
    outline = [t for t in outline if t[0] <= depth]

    prefix: list[str] = []

    for i, (level, title, startPage) in enumerate(outline):
        if depth != level:
            while len(prefix) >= level:
                prefix.pop()
            prefix.append(title)
        else:
            endPage: int
            if i < len(outline) - 1:
                endPage = outline[i + 1][2]
            else:
                endPage = input.page_count

            fullName = separator.join(prefix + [title])
            output: Document = Document("pdf", inputData)
            output.select(range(startPage - 1, endPage - 1))
            output.save(
                f"{outputDir}/{fullName}.pdf",
                garbage = 4,
                clean = True,
                deflate = True)

Split(arguments.filename, arguments.output_directory, arguments.separator, arguments.depth)