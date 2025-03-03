import os
from typing import Literal

type Year = Literal["Spec"] | int
type Paper = Literal["I", "II", "III"]
type Question = int
SPEC: Literal["Spec"] = "Spec"

def InclusiveRange(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))

def ToYear(year: int) -> Year:
    return year

def ToPaper(paper: int) -> Paper:
    return "I" if paper == 1 else "II" if paper == 2 else "III"

def ToYearString(year: Year) -> str:
    return "Spec" if year == SPEC else str(year)

def ToPaperString(paper: Paper) -> str:
    return paper

def ToQuestionString(question: Question) -> str:
    return str(question)

def ToYearDirectory(year: Year) -> str:
    return ToYearString(year)

def ToYearFile(year: Year) -> str:
    return f"{ToYearDirectory(year)}/{ToYearString(year)}.tex"

def ToPaperDirectory(year: Year, paper: Paper) -> str:
    return f"{ToYearDirectory(year)}/{ToPaperString(paper)}"

def ToPaperFile(year: Year, paper: Paper) -> str:
    return f"{ToPaperDirectory(year, paper)}/{ToPaperString(paper)}.tex"

def ToQuestionFile(year: Year, paper: Paper, question: Question) -> str:
    return f"{ToPaperDirectory(year, paper)}/{ToQuestionString(question)}.tex"

def Years() -> list[Year] :
    yearList: list[Year] = [ToYear(y) for y in InclusiveRange(1987, 2024)]
    yearList.append(SPEC)
    return yearList

def Papers(year: Year) -> list[Paper]:
    if isinstance(year, int):
        if year <= 2019:
            return [ToPaper(p) for p in InclusiveRange(1, 3)]
        else:
            return [ToPaper(p) for p in InclusiveRange(1, 2)]
    else:
        return [ToPaper(p) for p in InclusiveRange(1, 3)]
    
def Questions(year: Year, paper: Paper) -> list[Question]:
    if isinstance(year, int):
        if year <= 1993:
            return InclusiveRange(1, 16)
        elif year <= 2007:
            return InclusiveRange(1, 14)
        elif year <= 2018:
            return InclusiveRange(1, 13)
        else:
            if paper == "I":
                return InclusiveRange(1, 11)
            else:
                return InclusiveRange(1, 12)
    else:
        return InclusiveRange(1, 16)

def MakeYearFileContent(papers: list[Paper]) -> str:
    lines: list[str] = []
    lines.append("\\Year{\\currfilebase}")
    for paper in papers:
        paperString: str = ToPaperString(paper)
        lines.append(f"\\input{{\\currfiledir {paperString}/{paperString}}}")
    return os.linesep.join(lines)

def MakePaperFileContent(questions: list[Question]) -> str:
    lines: list[str] = []
    lines.append("\\Paper{\\currfilebase}")
    for question in questions:
        questionString: str = ToQuestionString(question)
        lines.append(f"\\input{{\\currfiledir {questionString}}}")
    return os.linesep.join(lines)

def MakeQuestionFileContent() -> str:
    return os.linesep.join(["\\Question{\\currfilebase}", "\\WorkInProgress"])

def CreateFiles(basePath: str) -> None:
    for year in Years():
        yearFileName: str = basePath + ToYearFile(year)
        yearPapers: list[Paper] = Papers(year)

        if not os.path.isdir(basePath + ToYearDirectory(year)):
            os.mkdir(basePath + ToYearDirectory(year))

        if not os.path.isfile(yearFileName):
            with open(yearFileName, "x") as file:
                file.write(MakeYearFileContent(yearPapers))

        for paper in yearPapers:
            paperFileName: str = basePath + ToPaperFile(year, paper)
            paperQuestions: list[Question] = Questions(year, paper)

            if not os.path.isdir(basePath + ToPaperDirectory(year, paper)):
                os.mkdir(basePath + ToPaperDirectory(year, paper))

            if not os.path.isfile(paperFileName):
                with open(paperFileName, "x") as file:
                    file.write(MakePaperFileContent(paperQuestions))

            for question in Questions(year, paper):
                questionFileName: str = basePath + ToQuestionFile(year, paper, question)

                if not os.path.isfile(questionFileName):
                    with open(questionFileName, "x") as file:
                        file.write(MakeQuestionFileContent())

if __name__ == "__main__":
    CreateFiles("./tex/")