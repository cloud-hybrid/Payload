---
title: gitHub Setup
layout: post
owner: Jacob B. Sanders
---

# Threading and Multiprocessing in Python

## Overview: Threading Vs. Multiprocessing
The threading module uses threads, the multiprocessing module uses processes. The difference is that threads run in the same memory space, while processes have separate memory. This makes it a bit harder to share objects between processes with multiprocessing. Since threads use the same memory, precautions have to be taken or two threads will write to the same memory at the same time. This is what the global interpreter lock is for.

- Multiprocessing use-cases seem to include more locally-bound (Intranet-based) IPCs & independent algorithmic computations where objects are file-scoped/globally accessible (bad, unless bytecode is encrypted, binarized, locked, hashed, etc.). However multiprocessing does have more dynamic overhead (RAM & Buffers) within shared spaces. These processes that're created in the buffer are killable/interruptible. 
- The use-cases for Threading include I/O bound operations such as GUI/interface responsiveness and when objects need to share the same memory space (removes the middle-man when compared to multiprocessing). Requires lower memory but is immutable on a kernal level.

## GIL with Threading/Multiprocessing

- Threading adheres to GIL
- Multiprocessing does not adhere to GIL

## Threading
- With I/O processes, such as webscraping or communicating with an external server/services where the CPU remains idle while waiting for the data, threading provides the program with additional processing power by executing multiple commands from multiple sources.
  - For example, lets say we need to download/retrieve data from multiple sources -- we can start multiple threads to bring in the requested data to the program's data space: ![Image description](.\Reference-Files\Data-Space-Threading.jpeg)

### Thread-Locking


