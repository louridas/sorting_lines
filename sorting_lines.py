import numpy as np
import matplotlib.pyplot as plt

import random

import argparse

trace = []

# Selection sort
def selection_sort(to_sort):
    n = len(to_sort)
    for i in range(0, n - 1):
        m = i
        for j in range(i + 1, n):
            if to_sort[j] < to_sort[m]:
                m = j
        to_sort[i], to_sort[m] = to_sort[m], to_sort[i]
        if not np.array_equal(np.array(to_sort), np.array(trace[-1])):
            trace.append(to_sort[:])
    return to_sort


# Insertion sort
def insertion_sort(to_sort, compare=lambda a, b: (a > b) - (a < b)):
    n = len(to_sort)
    for i in range(1, n):
        j = i
        while j > 0 and compare(to_sort[j-1], to_sort[j]) > 0:
            to_sort[j-1], to_sort[j] = to_sort[j], to_sort[j-1]
            j -= 1

        if not np.array_equal(np.array(to_sort), np.array(trace[-1])):
            trace.append(to_sort[:])
    return to_sort


# Merge sort
def merge(a, l, m, h, compare):

    c = []
    for k in range(l, h + 1):
        c.append(a[k])
    i = 0
    cm = m - l + 1
    ch = h - l + 1 
    j = cm
            
    for k in range(l, h + 1):
        if i >= cm:
            a[k] = c[j]
            j += 1
        elif j >= ch:
            a[k] = c[i]
            i += 1
        elif compare(c[i], c[j]) <= 0:
            a[k] = c[i]
            i += 1
        else:
            a[k] = c[j]
            j += 1

    if not np.array_equal(np.array(a), np.array(trace[-1])):
        trace.append(a[:])

def merge_sort(a, l, h, compare=lambda a, b: (a > b) - (a < b)):
    if l < h:
        m = l + (h - l) // 2
        merge_sort(a, l, m, compare)
        merge_sort(a, m + 1, h, compare)
        merge(a, l, m, h, compare)


# Quicksort
def partition(a, l, h, pathological=True):

    if not pathological:
        p = random.randint(l, h)
    else:
        p = a.index(min(a[l:h+1]))
    a[p], a[h] = a[h], a[p]
    b = l
    for i in range(l, h):
        if a[i] < a[h]:
            a[i], a[b] = a[b], a[i]
            b += 1
    a[b], a[h] = a[h], a[b]

    if not np.array_equal(np.array(a), np.array(trace[-1])):
        trace.append(a[:])

    return b, p
    
def quicksort(a, l, h):

    if l < h:
        p, pp = partition(a, l, h, False)
        quicksort(a, l, p-1)
        quicksort(a, p+1, h)


def draw_lines(trace, filename):
    
    # https://stackoverflow.com/a/8251668
    plt.style.use('dark_background')
    plt.figure(figsize=(len(trace) / 2, 5)) 
    trace_arr = np.array(trace)
    yy = []
    yy.append(np.arange(0, trace_arr.shape[1]))
    y = xsorted = trace_arr[0]
    for x in trace_arr[1:]:
        xsorted = np.argsort(x)
        ypos = np.searchsorted(x[xsorted], y)
        indices = xsorted[ypos]
        yy.append(indices)
    yy = np.array(yy)
    yy = yy.T
    xx = np.arange(0, trace_arr.shape[0])
    for line in yy:
        plt.plot(xx, line, #marker='o',
                 color='white',
                 linewidth=0.5, markersize=0.75)
    for i, ts in enumerate(to_sort_org):
        plt.plot(-.5, i, marker='o', color='white', markersize=ts/2 + 1)
    for i in range(len(to_sort_org)):
        plt.plot(xx[-1]+.5, i, marker='o', color='white',
                 markersize=i/2)    
    plt.axis('off')
    plt.gca().invert_yaxis()
    plt.savefig(filename)
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', help='image format', default='pdf')
args = parser.parse_args()

to_sort = list(range(1, 20+1))
random.shuffle(to_sort)
to_sort_org = to_sort[:]

trace = []
trace.append(to_sort[:])
selection_sort(to_sort[:])
print(len(trace))
draw_lines(trace, f'selection_sort_lines.{args.format}')
trace = []
trace.append(to_sort[:])
insertion_sort(to_sort[:])
print(len(trace))
draw_lines(trace, f'insertion_sort_lines.{args.format}')
trace = []
trace.append(to_sort[:])
merge_sort(to_sort[:], 0, len(to_sort) - 1)
print(len(trace))
draw_lines(trace, f'mergesort_lines.{args.format}')
trace = []
trace.append(to_sort[:])
quicksort(to_sort[:], 0, len(to_sort) - 1)
print(len(trace))
draw_lines(trace, f'quicksort_lines.{args.format}')
