import renpy
from renpy import ast
import io
import os

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

def calculate_tl_stats(source, target):
    if not os.path.exists(source):
        return None

    targetexists = os.path.exists(target)

    translator = renpy.game.script.translator
    language = renpy.game.preferences.language

    source_tls = set((tl for tl in translator.default_translates.values() if tl.filename.startswith(source)))
    source_tl_files = len(set((tl.filename for tl in source_tls)))

    source_tls_translated = set((tl for tl in source_tls if (language, tl.identifier) in translator.language_translates))
    source_tls_missing = source_tls - source_tls_translated

    if targetexists:
        target_tls = set((tl for (lang,_),tl in translator.language_translates.items() if lang == language and tl.filename.startswith(target)))
        target_tl_files = len(set((tl.filename for tl in target_tls)))
        excess_tls = len(set((tl for tl in target_tls if tl.identifier not in translator.default_translates)))

        return (source_tl_files, target_tl_files, len(source_tls), len(target_tls), len(source_tls_translated), len(source_tls_missing), excess_tls)
    else:
        return (source_tl_files, 0, len(source_tls), 0, len(source_tls_translated), len(source_tls_missing), 0)

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