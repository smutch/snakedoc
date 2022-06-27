rule separate_file:
    """
    This rule is in another file and is not included in the main Snakefile. We
    can still use the autodoc directive to generate docs for the whole file or
    just a single directive.

    :input: A file with some text in it.
    :output: Another file with some processing of the input text.
    """

    input:
        "output.txt"
    output:
        "output2.txt"
    shell:
        "echo 'output.txt content = ' > {output} && cat {input} >> {output}"
