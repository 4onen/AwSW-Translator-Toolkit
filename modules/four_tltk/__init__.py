import renpy
from renpy import ast
import renpy.translation.generation as gtl
import renpy.translation.scanstrings as stl
import io
import os
import re

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

def write_translate(language, filter, targetpath, tobj):
    fn = os.path.basename(tobj.filename)
    targetfn = os.path.join(targetpath, fn)

    file = gtl.open_tl_file(targetfn)

    file.write(u"# {}:{}\n".format(tobj.filename, tobj.linenumber))
    file.write(u"translate {} {}:\n".format(language, tobj.identifier.replace('.', '_')))
    file.write(u"\n")

    for n in tobj.block:
        file.write(u"    # " + n.get_code() + "\n")

    for n in tobj.block:
        file.write(u"    " + n.get_code(filter) + "\n")

    file.write(u"\n")


def get_sources(source):
    """
    Returns a list of source tl blocks that are to be translated.
    """

    default_translates = renpy.game.script.translator.default_translates
    
    return set((tl for tl in default_translates.values() if tl.filename.startswith(source)))

def get_translated(language, source_tls):
    """
    Returns a list of translated tl blocks.
    """
    language_translates = renpy.game.script.translator.language_translates

    return set((tl for tl in source_tls if (tl.identifier, language) in language_translates))

def get_targets(language, target):
    """
    Returns a list of target tl blocks that are already translated.
    """
    language_translates = renpy.game.script.translator.language_translates

    return set((tl for (_, lang),tl in language_translates.items() if lang == language and tl.filename.startswith(target)))

def calculate_tl_stats(source, target):
    if not os.path.exists(source):
        return None

    translator = renpy.game.script.translator
    language = renpy.game.preferences.language

    source_tls = get_sources(source)
    source_tl_files = len(set((tl.filename for tl in source_tls)))

    source_tls_translated = get_translated(language, source_tls)
    source_tls_missing = source_tls - source_tls_translated

    target_tls = get_targets(language, target)
    target_tl_files = len(set((tl.filename for tl in target_tls)))
    excess_tls = len(set((tl for tl in target_tls if tl.identifier not in translator.default_translates)))

    return (source_tl_files, target_tl_files, len(source_tls), len(target_tls), len(source_tls_translated), len(source_tls_missing), excess_tls)

def write_block_translations(source, target, filter):
    language = renpy.game.preferences.language

    source_tls = get_sources(source)
    source_tls_translated = get_translated(language, source_tls)
    source_tls_missing = source_tls - source_tls_translated

    for tl in sorted(source_tls_missing, key=lambda t: (t.filename, t.linenumber)):
        write_translate(language, filter, target, tl)


def translate_list_files_under(path):
    return [fn for fn in gtl.translate_list_files() if os.path.relpath(fn).startswith(path)]


def scan_strings(filename):
    """
    Scans `filename`, a file containing Ren'Py script, for translatable
    strings.

    Returns a list of TranslationString objects.
    """

    rv = [ ]

    for line, s in renpy.game.script.translator.additional_strings[filename]:  # @UndefinedVariable
        rv.append(stl.String(filename, line, s, False))

    for _filename, lineno, text in renpy.parser.list_logical_lines(filename):

        for m in re.finditer(stl.STRING_RE, text):

            s = m.group(1)
            if s is not None:
                s = s.strip()
                s = "u" + s
                s = eval(s)

                if s:
                    rv.append(stl.String(filename, lineno, s, False))

    return rv


def get_untranslated_strings(language, strings):
    """
    Returns a list of strings that are untranslated in `language`.
    """

    stl = renpy.game.script.translator.strings[language].translations

    return [s for s in strings if s not in stl]


def calculate_string_stats(source):
    language = renpy.game.preferences.language

    source_stl_files = translate_list_files_under(source)
    source_stl_strings = []

    for fn in source_stl_files:
        source_stl_strings.extend(scan_strings(fn))

    source_stl_strings_untranslated = len(get_untranslated_strings(language, source_stl_strings))
    source_stl_strings = len(source_stl_strings)
    source_stl_strings_translated = source_stl_strings - source_stl_strings_untranslated

    return (len(source_stl_files), source_stl_strings, source_stl_strings_translated, source_stl_strings_untranslated)


def write_string_translations(source, target, filter):
    raise NotImplementedError()