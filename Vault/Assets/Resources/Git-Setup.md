---
title: gitHub Setup
layout: post
---

# Git HTTPS Setup

## Prerequisites

- A Project created on gitHub.com.

## Setup

1. Within local repository, initialize with git.

```
git init
```

2. Add files and commit.

```
git add .

git add *

git commit -m "H3ll0 W0rld"

```

3. Add the remote repository.

```
git remote add origin https://github.com/cloud-hybrid/Cloud.git
```

4. Set the repository URL.

```
git remote set-url origin https://cloud-hybrid@github.com/cloud-hybrid/Cloud.git
```

5. Push and set the upstream.

```
git push --set-upstream origin master
```
