from distutils.core import setup

name="Novelwriting"
version="0.2.1"
DOCDIR="/usr/share/doc/%s-%s" % (name, version)
setup(
    name=name,
    version=version,
    description="Rule-based text generation",
    author="Jeff Epler",
    author_email="jepler@unpythonic.net",
    url="http://unpythonic.net/jeff/novelwriting/",
    packages=['novelwriting'],
    scripts=['scripts/novelwriting'],
    data_files=[(DOCDIR + "/examples",
                    [ "examples/buy.nw", "examples/nw.nw",
                      "examples/simple.nw", "examples/test.nw"]),
                (DOCDIR, ["README.html"])],
)
