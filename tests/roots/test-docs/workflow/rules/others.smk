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

rule other2:
    """
    This is other2...
    """

    input:
        "input.txt"
    output:
        "output.txt"
    shell:
        "cat {input} > {output} && echo {params.a} >> {output}"

rule other3:
    """
    This is other3...
    """

    input:
        "input.txt"
    output:
        "output.txt"
    shell:
        "cat {input} > {output} && echo {params.a} >> {output}"
