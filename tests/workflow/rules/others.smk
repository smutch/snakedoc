rule other:
    """
    This rule lies within another snakemake file. Looks familiar though!

    :input: an input file
    :output: an output file
    """

    input:
        "input.txt"
    output:
        "output.txt"
    shell:
        "cat {input} > {output} && echo {params.a} >> {output}"
