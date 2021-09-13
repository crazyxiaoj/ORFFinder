import sys
from Bio import SeqIO
from orffinder import orffinder

arguments = sys.argv
classed_arguments = {"orf_size": "75", "max_orfs_per_sequence": "-1", "remove_nested": "False", "trim_trailing": "False", "infmt": "fasta", "attr_name": "ORF_"}

try:
    for i in range(len(arguments)):

        argument = arguments[i]

        if argument.startswith("-"):

            classed_arguments[argument[1:]] = arguments[i + 1]

    sequences = SeqIO.parse(classed_arguments["in"], classed_arguments["infmt"])

    orf_size = int(classed_arguments["orf_size"])
    remove_nested = classed_arguments["remove_nested"] == "True"
    trim_trailing = classed_arguments["trim_trailing"] == "True"
    attr_name = classed_arguments["attr_name"]
    max_orfs_per_sequence = int(classed_arguments["max_orfs_per_sequence"])

    output = list()
    index = int()

    for sequence in sequences:

        seqname = sequence.description
        orfs = orffinder.getORFs(sequence, minimum_length=orf_size, trim_trailing=trim_trailing, remove_nested=remove_nested)

        local_index = int()
        for orf in orfs:

            index += 1
            local_index += 1
            output.append([seqname, "ORFFinder Python", "ORF", str(orf["start"]), str(orf["end"]), ".", orf["sense"], str(orf["frame"] - 1), "orf_id \"" + attr_name + str(index) + "\""])

            if local_index >= max_orfs_per_sequence and max_orfs_per_sequence != -1:
                break


    full_output = "\n".join(["\t".join(x) for x in output])

    if "out" not in classed_arguments.keys():

        print(full_output)

    else:

        open(classed_arguments["out"], "w+").write(full_output)

except:
    print("USAGE\n  orffinder-to-gtf [-in input] [-infmt format] [-out output] [-orf_size int]\n    [-remove_nested boolean] [-trim_trailing boolean] [-max_orfs_per_sequence int]\n    [-attr_name string]\n\nDESCRIPTION\n  ORFFinder Python v1.5\n\nUse '-help' to print detailed descriptions of command line arguments\n========================================================================")
