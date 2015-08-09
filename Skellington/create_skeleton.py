
import os, shutil, pprint
join = os.path.join


def move(p0, p1):
    print ("moving... %s %s" % (p0, p1))
    os.rename(p0, p1)


def replace_vars_in_file(fname, shortname, replace_vars):
    fpath = join(shortname, fname)
    print ("opening file:%s: for reading" % fpath)
    f = open(fpath, "rb")
    data = f.read()
    f.close()
    for varname, varvalue in replace_vars.items():
	data = data.replace("yourgame" + varname, varvalue)

    print ("opening file:%s: for writing" % fpath)
    f = open(fpath, "wb")
    f.write(data)
    f.close()


def create_files(shortname="", authors = "", url = "", description = "", short_licence = ""):
    if not url:
	url = 'http://pyweek.org/e/' + shortname

    replace_vars = dict(shortname = shortname, 
		authors = authors,
		url = url,
		description = description,
		short_licence = short_licence)
    pprint.pprint(replace_vars)

    shutil.copytree("templatefiles", shortname)
    move(join(shortname, "yourgamedir"), join(shortname, shortname))

    # replace some variables inside files.
    fnames_to_replace = ["setup.py", "android.txt", "run_game.py",
	"LICENSE.txt", "README.txt", "Makefile",
	join("scripts", "yourgameshortname")]

    for fname in fnames_to_replace:
	replace_vars_in_file(fname, shortname, replace_vars)

    # move the script over.
    move(join(shortname, "scripts", "yourgameshortname"), join(shortname, "scripts", shortname))


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser("see --help for options")
    parser.add_option("-s", "--shortname", dest="shortname",
		      help="shortname")
    parser.add_option("-a", "--authors",
		      dest="authors", default="",
		      help="authors")
    parser.add_option("-u", "--url",
		      dest="url", default="",
		      help="url")
    parser.add_option("-d", "--description",
		      dest="description", default="",
		      help="a short one line description")
    parser.add_option("-l", "--short_licence",
		      dest="short_licence", default="",
		      help="a short licence eg, LGPL GPL or BSD")

    (options, args) = parser.parse_args()

    options_dict = vars(options)

    if options_dict["shortname"] is None:
	parser.error("need a shortname")
    if os.path.exists(options_dict["shortname"]):
	parser.error(":%s: path exists" % options_dict["shortname"])

    create_files(**vars(options))


# vim: set filetype=python sts=4 sw=4 noet si :
