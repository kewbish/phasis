from collections import defaultdict
from datetime import datetime, timedelta
from os import listdir, path, stat
from spacy import load
from spacy.tokens import DocBin
from spacy.tokens.doc import Doc
from dateparser import parse as date_parse
from yaspin import yaspin
import click
import warnings
from colorama import init, Fore
from git import Repo
from typing import List, Tuple

DIR = "/home/kewbish/EVB/dev/lc/"
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


class Phasis:
    def __init__(self) -> None:
        self.spinner = yaspin(text="Loading Phasis ...")
        self.spinner.start()
        self.nlp = load("en_core_web_sm")
        Doc.set_extension("file_source", default=None)

        if not path.isfile("./em.phasis"):
            files = [(open(DIR + f).read(), f) for f in listdir(DIR)]

            doc_bin = DocBin(store_user_data=True)

            file_dates = defaultdict(list)
            for doc, context in self.nlp.pipe(files, as_tuples=True):
                for ent in doc.ents:
                    if ent.label_ == "DATE":
                        file_dates[context].append(ent)
                doc._.file_source = context
                doc_bin.add(doc)

            self.spinner.stop()
            self.file_dates = file_dates

            doc_bin.to_disk("./em.phasis")
        else:
            doc_bin = DocBin().from_disk("./em.phasis")
            timeline = []

            for doc in self.nlp.pipe(doc_bin.get_docs(self.nlp.vocab)):
                for ent in doc.ents:
                    if ent.label_ == "DATE":
                        parsed_date = date_parse(ent.text, settings={"RELATIVE_BASE": datetime.now()})
                        parsed_date = parsed_date.date() if parsed_date else parsed_date
                        # parsed_date = date_parse(
                        #     ent.text, settings={"RELATIVE_BASE": datetime.fromtimestamp(stat(DIR + doc._.file_source).st_mtime)}
                        # )
                        if parsed_date:
                            timeline.append((parsed_date, doc._.file_source))
                doc_bin.add(doc)
            timeline.sort()
            self.timeline = timeline

            self.spinner.stop()


def fore_from_hex(hexcode: str) -> str:
    """print in a hex defined color"""
    hexint = int(hexcode[1:], 16)
    return "\x1B[38;2;{};{};{}m".format(hexint >> 16, hexint >> 8 & 0xFF, hexint & 0xFF)


def print_timeline(timeline: List[Tuple]) -> None:
    i = 0
    while i < len(timeline):
        current_date = timeline[i][0]
        to_print = []
        to_print.append(current_date.strftime(f"{fore_from_hex('#C3B1E1')}%d %B %Y{Fore.RESET}"))
        while i < len(timeline) and current_date == timeline[i][0]:
            if len(timeline[i]) == 2:
                to_print.append(f"    - {timeline[i][1]} {fore_from_hex('#91DDF2')}(mention){Fore.RESET}")
            elif timeline[i][2] == "CREATE":
                to_print.append(f"    - {timeline[i][1]} {fore_from_hex('#ADDFB3')}(birth){Fore.RESET}")
            elif timeline[i][2] == "DEATH":
                to_print.append(f"    - {timeline[i][1]} {fore_from_hex('#CB4154')}(death){Fore.RESET}")
            elif timeline[i][2] == "MODIF":
                to_print.append(f"    - {timeline[i][1]} {fore_from_hex('#F5AD89')}(modified){Fore.RESET}")
            elif timeline[i][2] == "SICK":
                to_print.append(f"    - {timeline[i][1]} {fore_from_hex('#F1FF55')}(sick){Fore.RESET}")
            i += 1
        if len(to_print) > 1:
            for tp in to_print:
                print(tp)


def gen_timeline(death: int, sick: int, to_add: List = []):
    creation_times = []
    for f in listdir(DIR):
        c_time = datetime.fromtimestamp(stat(DIR + f).st_ctime).date()
        m_time = datetime.fromtimestamp(stat(DIR + f).st_mtime).date()
        has_died = (datetime.now().date() - m_time).days > death
        is_sick = (datetime.now().date() - m_time).days > sick
        creation_times.append((c_time, f, "CREATE"))
        if m_time != c_time:
            creation_times.append((m_time, f, "MODIF"))
        # if a file has died, don't mark it as sick
        if has_died:
            creation_times.append((m_time + timedelta(days=death), f, "DEATH"))
        elif is_sick:
            creation_times.append((m_time + timedelta(days=sick), f, "SICK"))
    final_timeline = to_add + creation_times
    final_timeline.sort()
    return final_timeline


@click.command()
@click.option("--death", default=14, help="Number of days after which a file is declared dead.")
@click.option("--sick", default=10, help="Number of days after which a file needs more attention.")
def show_timeline(death: int, sick: int, to_print: bool = True):
    phasis = Phasis()
    if not phasis.timeline:
        print("No timeline yet...")
        return
    phasis.spinner.text = "Loading obituaries and nativities..."
    phasis.spinner.start()
    final_timeline = gen_timeline(death, sick, phasis.timeline)
    phasis.spinner.stop()
    print_timeline(final_timeline)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(context):
    if not context.invoked_subcommand:
        gen_timeline()


@cli.command(name="get_sick")
@click.option("--death", default=14, help="Number of days after which a file is declared dead.")
@click.option("--sick", default=10, help="Number of days after which a file needs more attention.")
def get_sick(death: int, sick: int):
    spinner = yaspin(text="Checking for symptoms ...")
    spinner.start()
    creation_times = []
    for f in listdir(DIR):
        m_time = datetime.fromtimestamp(stat(DIR + f).st_mtime).date()
        is_sick = sick < (datetime.now().date() - m_time).days < death
        if is_sick:
            creation_times.append((m_time + timedelta(days=sick), f, "SICK"))
    creation_times.sort()
    spinner.stop()
    print_timeline(creation_times)


@cli.command(name="gittt")
def git_time_travel():
    nlp = load("en_core_web_sm")
    repo = Repo.init("/".join(DIR.split("/")[:-3]))
    recent_commits = list(repo.iter_commits("master", max_count=10))
    print("Time Travelling...")
    dates = defaultdict(list)
    for i in range(1, len(recent_commits)):
        # print(recent_commits[i].message)
        diff = recent_commits[i - 1].diff(recent_commits[i])
        for diff_item in diff.iter_change_type("M"):
            contents = diff_item.a_blob.data_stream.read().decode("utf-8")
            doc = nlp(contents)
            for ent in doc.ents:
                if ent.label_ == "DATE":
                    dates[recent_commits[i].committed_date].append(ent.text)
            # print(f"    {fore_from_hex('#ADDFB3')}+ {contents}{Fore.RESET}")
            # print(f"    {fore_from_hex('#CB4154')}- {diff_item.b_blob.data_stream.read().decode('utf-8')}{Fore.RESET}")
    dates = dict(sorted(dates.items()))
    for key, value in dates.items():
        print(key)
        for v in value:
            print(f"    - {v} {fore_from_hex('#91DDF2')}(mention){Fore.RESET}")


if __name__ == "__main__":
    init()
    cli()
