# README #

This is the repository that you will use at the starting point for the FRI Data Science Project Competition. In this readme file you will find short instructions for the most important tasks that are ahead of you.

## Branching ##

Repository currently has two branches, the `master` branch and the `develop` branch.

The code on the `master` branch should at all times be clean, well commented and stable/working. Meaning that if your advisors or graders want to check the state of the project, they can use the code that is currently on the `master` branch.

All the coding and writing work should be done on the `develop` branch, or on additional newly created branches. When you reach a milestone in the development, your code is stable and well commented, you should merge the `develop` branch (or any other branches you created) into the `master` branch and the tag the `master` as a new version. Initial tag of the `master` branch is 0.1. Increase the second number for minor/small changes and the first number for major/big changes in the codebase. This way the whole team, along with the advisors and graders will have a complete history and overview of the project's progress.

You can do all of the above manually, or you can use git flow. Git flow is a branching model that is commonly used in industry and academia ([https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow), [https://www.youtube.com/watch?v=6LhTe8Mz6jM](https://www.youtube.com/watch?v=6LhTe8Mz6jM)). By using git flow you can use special git flow commands that will ease the process for you. It is even integrated into most popular git GUIs, e.g. Sourcetree ([https://www.youtube.com/watch?v=z53JJ7P78Vc](https://www.youtube.com/watch?v=z53JJ7P78Vc)) and GitKraken ([https://www.youtube.com/watch?v=eTOgjQ9o4vQ](https://www.youtube.com/watch?v=eTOgjQ9o4vQ)).

## Folder structure ##

There are several subfolders in the repository:

* the source folder (`/src`),
* the journal folder (`/journal`),
* the interim report folder (`/interim_report`),
* the final report folder (`/final_report`),
* and the presentation folder (`/presentation`).

### The source folder ###

All your source code should go into this folder. How you structure things (e.g. via subfolders) inside there is completely up to you.

### The journal folder ###

In this folder you will find a template journal file. Replace John Doe's name and surname with your own. If you are part of a team, each student should have his own journal file, so make a copy of the template journal file and rename it appropriately. Inside the journal file are some example entries into the journal. Every time you do something, be it watching tutorials, reading literature, or coding, make a journal entry and describe in a few sentences what exactly you did or what you learnt.

### The interim report folder ###

In this folder you can find the LaTeX template for both reports. You will write the report by using the `report.tex` file. In this file you can initially find examples of several commonly used report elements (e.g. tables, figures, lists, equations ...). When writing your report replace these contents with your own. The interim report should not be longer than two pages.

### The final report folder ###

To write the final report copy the interim report files from the interim report folder to the final report folder and change the Archive parameter to the correct version (you can find this on the top of the .tex file under the article information section). This way you will be able to upgrade your interim report into the final report. The final report should not be longer than four pages.

### The presentation folder ###

Put the document or documents for your final presentation into this folder.
