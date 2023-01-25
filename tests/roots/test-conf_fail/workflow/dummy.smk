rule dummy1:
    """
    This is a dummy rule.

    :input: an input file
    :output: an output file
    :config omega_m:
        The matter density
    """

    input:
        "input.txt"
    output:
        "output.txt"
    shell:
        "cat {input} > {output} && echo {params.omega_m} >> {output}"
