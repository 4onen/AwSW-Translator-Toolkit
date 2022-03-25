import renpy
from renpy import ast
import io

def get_untranslated_info_line(tobj):
    contents = ""
    if tobj.block and (tobj.block[0].translatable or isinstance(tobj.block[0], ast.Say)):
        contents = tobj.block[0].get_code()

    return u'{}:{}:\t\t{}\t:\t{}\n'.format(tobj.filename, tobj.linenumber, tobj.identifier, contents)

def make_untranslated_txt(language):
    """
    Prints a list of missing translations for `language`.
    """

    translator = renpy.game.script.translator

    missing_translates = set()

    for tlblockid, translate in translator.default_translates.items():
        if (tlblockid, language) not in translator.language_translates:
            missing_translates.add(translate)

    with io.open('untranslated.txt','w',encoding='utf-8') as f:
        for line in sorted(map(get_untranslated_info_line, missing_translates)):
            f.write(line)

def make_overtranslated_txt(language):
    """
    Prints a list of translations lacking basegame nodes for `language`.
    """

    translator = renpy.game.script.translator

    excess_translates = set()

    for (tlblockid, l), translate in translator.language_translates.items():
        if l != language:
            continue
        if tlblockid in translator.default_translates:
            continue
        excess_translates.add(translate)

    with io.open('overtranslated.txt','w',encoding='utf-8') as f:
        for line in sorted(map(get_untranslated_info_line, excess_translates)):
            f.write(line)

def write_translate(language, filter, file, translate):
    file.write(u"# {}:{}\n".format(translate.filename, translate.linenumber))
    file.write(u"translate {} {}:\n".format(language, translate.identifier.replace('.', '_')))
    file.write(u"\n")

    for n in translate.block:
        file.write(u"    # " + n.get_code() + "\n")

    for n in translate.block:
        file.write(u"    " + n.get_code(filter) + "\n")

    file.write(u"\n")


# def write_translates(filename, language, filter):  # @ReservedAssignment

#     fn, common = shorten_filename(filename)

#     # The common directory should not have dialogue in it.
#     if common:
#         return

#     tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, fn)

#     if tl_filename[-1] == "m":
#         tl_filename = tl_filename[:-1]

#     if language == "None":
#         language = None

#     translator = renpy.game.script.translator

#     for label, t in translator.file_translates[filename]:

#         if (t.identifier, language) in translator.language_translates:
#             continue

#         f = open_tl_file(tl_filename)

#         if label is None:
#             label = ""

#         write_translate(language, filter, f, t)