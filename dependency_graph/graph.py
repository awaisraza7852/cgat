"""
Read snakefood dependencies and output a visual graph.
"""
# This file is part of the Snakefood open source package.
# See http://furius.ca/snakefood/ for licensing details.

# Modified by AH to colour nodes according to subdir.

import sys
import os

from snakefood.depends import read_depends, eliminate_redundant_depends

prefix = '''
# This file was generated by sfood-graph.

strict digraph "dependencies" {
    graph [
        rankdir = "LR",
        overlap = "scale",
        size = "8,10",
        ratio = "fill",
        fontsize = "16",
        fontname = "Helvetica",
        clusterrank = "local"
        ]

       node [
           fontsize=%s
           shape=ellipse
           // style=filled
           // shape=box
       ];

'''
postfix = '''

}
'''

COLORS = ["#999999", "#E69F00", "#56B4E9", "#009E73",
          "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]


def graph(pairs, write, fontsize, color_map):
    "Given (from, to) pairs of (root, fn) files, output a dot graph."
    write(prefix % fontsize)
    for (froot, f), (troot, t) in pairs:
        if opts.pythonify_filenames:
            f = normpyfn(f)
            t = normpyfn(t)
        if opts.full_pathnames:
            f = os.path.join(froot, f)
            if troot:
                t = os.path.join(troot, t)
        if troot is None:
            dn = os.path.dirname(f)
            if dn not in color_map:
                color_map[dn] = COLORS[len(color_map) % len(COLORS)]
            write('"%s"  [style=filled, color="%s"];\n' % (f, color_map[dn]))
        else:
            write('"%s" -> "%s";\n' % (f, t))
    write(postfix)


def normpyfn(fn):
    "Normalize the python filenames for output."
    if fn is None:
        return fn
    if fn.endswith('.py'):
        fn = fn[:-3]
    fn = fn.replace(os.sep, '.')
    return fn


def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())

    parser.add_option('-f', '--full-pathnames', '--full', action='store_true',
                      help="Output the full pathnames, not just the relative.")

    parser.add_option('-p', '--pythonify-filenames', '--remove-extensions',
                      action='store_true',
                      help="Remove filename extensions in the graph and "
                      "replace slashes with dots.")

    parser.add_option('-r', '--redundant', action='store_false', default=True,
                      help="Do not eliminate redundant dependencies.")

    parser.add_option('--fontsize', action='store', type='int',
                      default=10,
                      help="The size of the font to use for nodes.")

    global opts
    opts, args = parser.parse_args()

    if not args:
        args = ['-']

    color_map = {}

    for fn in args:
        if fn == '-':
            f = sys.stdin
        else:
            f = open(fn)
        depends = read_depends(f)
        if opts.redundant:
            depends = eliminate_redundant_depends(depends)
        graph(depends, sys.stdout.write, opts.fontsize, color_map)


if __name__ == "__main__":
    main()

