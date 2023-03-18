from collections import defaultdict
from datetime import date, datetime, timedelta
from os import path, stat
from glob import iglob
from pickle import dump
from pickle import load as pickle_load
from spacy import load
from spacy.tokens import DocBin
from spacy.tokens.doc import Doc
from dateparser import parse as date_parse
from yaspin import yaspin
import click
import warnings
from colorama import init, Fore
from git import Diff
from git.repo import Repo
from typing import List, Tuple
from dataclasses import dataclass
from chatgpt_wrapper import ChatGPT
from json import loads
from difflib import Differ, context_diff

DIR = "/home/kewbish/EVB/"
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
            files = [(open(f).read(), f) for f in iglob(DIR + "**/*.md", recursive=True)]

            doc_bin = DocBin(store_user_data=True)
            timeline = []

            file_dates = defaultdict(list)
            for doc, context in self.nlp.pipe(files, as_tuples=True):
                for ent in doc.ents:
                    if ent.label_ == "DATE":
                        file_dates[context].append(ent)
                        parsed_date = date_parse(ent.text, settings={"RELATIVE_BASE": datetime.now()})
                        parsed_date = parsed_date.date() if parsed_date else parsed_date
                        if parsed_date:
                            timeline.append((parsed_date, doc._.file_source))
                doc._.file_source = context
                doc_bin.add(doc)

            timeline.sort()
            self.timeline = timeline
            self.spinner.stop()
            self.file_dates = file_dates

            doc_bin.to_disk("./em.phasis")
        elif not path.isfile("./tl.phasis"):
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
            with open("./tl.phasis", "wb") as x:
                dump(timeline, x)

            self.spinner.stop()
        else:
            with open("./tl.phasis", "rb") as x:
                self.timeline = pickle_load(x)
            self.spinner.stop()


@dataclass()
class PhasisDiff:
    revision: str
    message: str
    diff_contents_a: str | None = None
    diff_contents_b: str | None = None


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


def gen_timeline(death: int, sick: int, to_add: List = [], no_translate: bool = False):
    creation_times = []
    for f in iglob(DIR + "**/*.md", recursive=True):
        c_time = datetime.fromtimestamp(stat(f).st_ctime).date()
        m_time = datetime.fromtimestamp(stat(f).st_mtime).date()
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
    if no_translate:
        final_timeline = list(map(lambda x: (x[0].strftime("%s"), x[1], x[2]), final_timeline))
    return final_timeline


@click.group(invoke_without_command=True)
@click.pass_context
def cli(context):
    if not context.invoked_subcommand:
        show_timeline(14, 10)


@cli.command(name="timeline")
@click.option("--death", default=14, help="Number of days after which a file is declared dead.")
@click.option("--sick", default=10, help="Number of days after which a file needs more attention.")
def show_timeline(death: int, sick: int):
    phasis = Phasis()
    if not phasis.timeline:
        print("No timeline yet...")
        return
    phasis.spinner.text = "Loading obituaries and nativities..."
    phasis.spinner.start()
    final_timeline = gen_timeline(death, sick, phasis.timeline)
    phasis.spinner.stop()
    print_timeline(final_timeline)


@cli.command(name="get_sick")
@click.option("--death", default=14, help="Number of days after which a file is declared dead.")
@click.option("--sick", default=10, help="Number of days after which a file needs more attention.")
def get_sick(death: int, sick: int):
    spinner = yaspin(text="Checking for symptoms ...")
    spinner.start()
    creation_times = []
    for f in iglob(DIR + "**/*.md", recursive=True):
        m_time = datetime.fromtimestamp(stat(f).st_mtime).date()
        is_sick = sick < (datetime.now().date() - m_time).days < death
        if is_sick:
            creation_times.append((m_time + timedelta(days=sick), f, "SICK"))
    creation_times.sort()
    spinner.stop()
    print_timeline(creation_times)


@cli.command(name="gittt")
def git_time_travel():
    nlp = load("en_core_web_sm")
    repo = Repo.init(DIR)
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


@cli.command(name="gitcd")
@click.option("--path", help="Path of file to search commits for")
@click.option("--amt", default=5, help="Amount of commits to return")
def click_git_commit_diffs(path: str, amt: int):
    print("\n".join([pdiff.__repr__() for pdiff in git_commit_diffs(path, amt)]))


def git_commit_diffs(
    path: str, amt: int, commit_head: str | None = None, commit_date: date | None = None
) -> List[PhasisDiff]:
    repo = Repo.init(DIR)
    config = {"max_count": amt, "paths": path}
    if commit_date:
        config["after"] = commit_date.strftime("%b %e %Y")
        config["before"] = (commit_date + timedelta(days=1)).strftime("%b %e %Y")
    recent_commits = list(repo.iter_commits(commit_head if commit_head else "master", **config))
    pdiffs = []
    for commit in recent_commits:
        diffs = commit.diff(commit.parents[0])
        diffs: List[Diff] = list(filter(lambda diff_f: diff_f.a_path == path.replace(DIR, ""), diffs))
        if len(diffs) <= 0:
            return []
        pdiff = PhasisDiff(commit.hexsha, commit.message)
        a_blob_stream = diffs[0].a_blob
        if a_blob_stream:
            pdiff.diff_contents_a = a_blob_stream.data_stream.read().decode("utf-8")
        b_blob_stream = diffs[0].b_blob
        if b_blob_stream:
            pdiff.diff_contents_b = b_blob_stream.data_stream.read().decode("utf-8")
        new_a, new_b = "", ""
        if pdiff.diff_contents_a is not None and pdiff.diff_contents_b is not None:
            for diff in list(Differ().compare(pdiff.diff_contents_a.splitlines(), pdiff.diff_contents_b.splitlines())):
                if not diff:
                    continue
                for l in diff.splitlines():
                    if l.startswith("-"):
                        new_b += l[2:]
                    else:
                        new_a += l[2:]
            pdiff.diff_contents_a = new_a
            pdiff.diff_contents_b = new_b
        pdiffs += [pdiff]
    return pdiffs


@cli.command(name="gitfd")
@click.option("--path", help="Path of file to search commits for")
@click.option("--commit", help="Commit SHA to search from", default=None)
def click_git_fetch_diff(path: str, commit: str | None = None):
    diffs = git_commit_diffs(path, 1, commit)
    print(fetch_from_chatgpt(diffs[0]))


def fetch_from_chatgpt(diff: PhasisDiff) -> str:
    if not diff.diff_contents_a or not diff.diff_contents_b:
        return "Note created or deleted - no insights found!"
    bot = ChatGPT()
    prompt = f"""You are a personal knowledge management expert. My goal is to learn how my ideas change over time and why they change. Summarize the change in the points of view in two sentences. Then, ask an open-ended question about the difference in ideas. The notes are labelled "Before" and "After" below. Address your response to "you".

For example, you would write "Before, you thought that the best approach to solving the problem was to divide and conquer. After, you used recursion and added a note to check your work with a friend."

---

Before: "{diff.diff_contents_a[:350] if diff.diff_contents_a else ''}"

After: "{diff.diff_contents_b[:350] if diff.diff_contents_b else ''}"
    """
    response = bot.ask(prompt)
    if not response:
        return ""
    bot._cleanup()
    return response


if __name__ == "__main__":
    init()
    cli()
