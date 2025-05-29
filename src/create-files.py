import os
from typing import Final

type Year = int
type Paper = int
type Question = int
SPEC: Final[Year] = 0

def InclusiveRange(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))

def Years() -> list[Year] :
    # yearList: list[Year] = [SPEC] + [y for y in InclusiveRange(1987, 2024)]
    # return yearList
    return [2020, 2021, 2022, 2023, 2024]

def Papers(year: Year) -> list[Paper]:
    if year == SPEC or year <= 2019:
        return [p for p in InclusiveRange(1, 3)]
    else:
        return [p for p in InclusiveRange(2, 3)]
    
def Questions(year: Year, paper: Paper) -> list[Question]:
    if year == SPEC or year <= 1993:
        return InclusiveRange(1, 16)
    elif year <= 2007:
        return InclusiveRange(1, 14)
    elif year <= 2018:
        return InclusiveRange(1, 13)
    else:
        if paper == 1:
            return InclusiveRange(1, 11)
        else:
            return InclusiveRange(1, 12)

def MakeYearFileContent(papers: list[Paper]) -> str:
    lines: list[str] = []
    lines.append("\\Year{\\currfilebase}")
    for paper in papers:
        lines.append("\\input{" + f"\\currfiledir\\currfilebase/{paper}" + "}")
    return os.linesep.join(lines)

def MakePaperFileContent(questions: list[Question]) -> str:
    lines: list[str] = []
    lines.append("\\Paper{\\currfilebase}")
    for question in questions:
        lines.append("\\input{" + f"\\currfiledir\\currfilebase/{question}" + "}")
    return os.linesep.join(lines)

def MakeQuestionFileContent() -> str:
    return os.linesep.join(["\\Question{\\currfilebase}", "\\WorkInProgress"])

def WriteIfNotExist(basePath: str, directory: str, fileName: str, content: str) -> None:
    fullPath: str = basePath + directory + fileName

    if not os.path.isfile(fullPath):
        with open(fullPath, "x") as file:
            file.write(content)

def CreateIfNotExist(basePath: str, directory: str) -> None:
    fullDirectory: str = basePath + directory

    if not os.path.isdir(fullDirectory):
        os.mkdir(fullDirectory)

def CreateFiles(basePath: str) -> None:
    CreateIfNotExist(basePath, "")

    for year in Years():
        yearPapers: list[Paper] = Papers(year)
        yearFileName: str = f"{year}.tex"

        WriteIfNotExist(basePath, "", yearFileName, MakeYearFileContent(yearPapers))

        paperDirectory: str = f"{year}/"
        CreateIfNotExist(basePath, paperDirectory)

        for paper in yearPapers:
            paperQuestions: list[Question] = Questions(year, paper)
            paperFileName: str = f"{paper}.tex"

            WriteIfNotExist(basePath, paperDirectory, paperFileName, MakePaperFileContent(paperQuestions))
            
            questionDirectory: str = paperDirectory + f"{paper}/"
            CreateIfNotExist(basePath, questionDirectory)

            for question in Questions(year, paper):
                questionFileName: str = f"{question}.tex"

                WriteIfNotExist(basePath, questionDirectory, questionFileName, MakeQuestionFileContent())

if __name__ == "__main__":
    CreateFiles("./tex/")