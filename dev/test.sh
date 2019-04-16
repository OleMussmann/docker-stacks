#!/bin/bash

r="""first
| Miniconda | 1.2.3 |
last"""

echo "$r" | grep "Miniconda" | awk -F'|' '{print $3}' | xargs

