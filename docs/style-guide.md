# IEEE-Computer Style Guide

This is a IEEE-Computer Style Guide inspired by [*Git Style Guide*](https://github.com/agis/git-style-guide/blob/master/README.md) it was modified by @malkam03 removing some of the contents.

# Table of contents

1. [Branches](#branches)
2. [Commits](#commits)

## Branches

* Choose *short* and *descriptive* preceded by the following types of branch:
  - ft-short-descriptive: for feature branches(from and merge to develop).
  - bg-short-descriptive: for bug branches(from and merge to develop).
  - hf-short-descriptive: for hot fixes branches(form and merge to master).
  - junk-short-descriptive: for junk branches(will never merge).

  ```shell
  # good
  $ git checkout -b ft-oauth-migration

  # bad - too vague
  $ git checkout -b login_fix
  ```

* Identifiers from corresponding tickets in an external service (eg. a GitHub
  issue) are also good candidates for use in branch names. For example:

  ```shell
  # GitHub issue #15
  $ git checkout -b ft-issue-15
  $ git checkout -b bg-issue-15
  $ git checkout -b hf-issue-15
  ```

* Use *hyphens* to separate words.

* When several people are working on the *same* feature, it might be convenient
  to have *personal* feature branches and a *team-wide* feature branch.
  Use the following naming convention:

  ```shell
  $ git checkout -b ft-chapter-benefits/master # team-wide branch
  $ git checkout -b ft-chapter-benefits/jane  # Jane's personal branch
  $ git checkout -b ft-chapter-benefits/john   # John's personal branch
  ```

  Merge at will the personal branches to the team-wide branch (see ["Merging"](#merging)).
  Eventually, the team-wide branch will be merged to "master".

* Delete your branch from the upstream repository after it's merged, unless
  there is a specific reason not to.

  Tip: Use the following command while being on "master", to list merged
  branches:

  ```shell
  $ git branch --merged | grep -v "\*"
  ```

## Commits

* Each commit should be a single *logical change*. Don't make several
  *logical changes* in one commit. For example, if a patch fixes a bug and
  optimizes the performance of a feature, split it into two separate commits.

  *Tip: Use `git add -p` to interactively stage specific portions of the
  modified files.*

* Don't split a single *logical change* into several commits. For example,
  the implementation of a feature and the corresponding tests should be in the
  same commit.

* Commit *early* and *often*. Small, self-contained commits are easier to
  understand and revert when something goes wrong.

* Commits should be ordered *logically*. For example, if *commit X* depends
  on changes done in *commit Y*, then *commit Y* should come before *commit X*.

Note: While working alone on a local branch that *has not yet been pushed*, it's
fine to use commits as temporary snapshots of your work. However, it still
holds true that you should apply all of the above *before* pushing it.

# License

![cc license](http://i.creativecommons.org/l/by/4.0/88x31.png)

This work is licensed under a [Creative Commons Attribution 4.0
International license](https://creativecommons.org/licenses/by/4.0/).

# Acknowledgement

Agis Anastasopoulos / [@agisanast](https://twitter.com/agisanast) / http://agis.io
... and [contributors](https://github.com/agis-/git-style-guide/graphs/contributors)!
