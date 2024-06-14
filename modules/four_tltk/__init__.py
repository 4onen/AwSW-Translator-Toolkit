import renpy
from renpy import ast
from renpy.translation import quote_unicode
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

language_mod_init_template = u"""
# -*- coding: utf-8 -*-
from modloader.modclass import Mod, loadable_mod
@loadable_mod
class AWSWMod(Mod):
    name = "{}" # TODO: More human-readable name
    version = "1.0"
    author = "Translator's Toolkit" # TODO: Your (team?) name!
    dependencies = ["MagmaLink"]
    @staticmethod
    def mod_load():
        import jz_magmalink as ml
        c = (
            ml.find_label("splashscreen")
            .search_if('persistent.lang == "Jp"')
        )
        (
            c
            .branch()
            .search_menu()
            .add_choice(text=u"{}", jump="tltk_gen_language_mod_{}")
        )
        (
            c
            .branch_else()
            .search_menu()
            .add_choice(text=u"{}", jump="tltk_gen_language_mod_{}")
        )
        c.link_behind_from("tltk_gen_language_mod_{}_end")
    @staticmethod
    def mod_complete():
        pass
"""

language_mod_rpy_template = u"""
label tltk_gen_language_mod_{}:
    $ renpy.change_language("{}")
    jump tltk_gen_language_mod_{}_end
"""

def generate_base_game_language_mod(language_name):
    """
    Generates a base language mod for the given language.
    """
    mod_folder = "game/mods/{}_mod".format(language_name)
    if not os.path.exists(mod_folder):
        os.makedirs(mod_folder)

    mod_info = os.path.join(mod_folder, "__init__.py")
    with io.open(mod_info, "w", encoding="utf-8") as f:
        f.write(language_mod_init_template.format(language_name, language_name, language_name, language_name, language_name, language_name))
    with io.open(os.path.join(mod_folder, "tltk_gen_language_mod_{}.rpy".format(language_name)), "w", encoding="utf-8") as f:
        f.write(language_mod_rpy_template.format(language_name, language_name, language_name))
    return mod_folder

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
    files = [fn for fn in gtl.translate_list_files() if os.path.relpath(fn).startswith(path)]
    return files


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

    return [s for s in strings if s.text not in stl]


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

string_translation_template_start = u"""
%s
    # These string translations were generated by the AwSW Translator's Toolkit.
    # The entries are in the form of:
    #  old_string: (new_string, elided_file_path, line_number) 
    # Edit the `new_string` to provide a translation.
    # The `elided_file_path` and `line_number` are provided for reference.

    # Note that, if the `old_string` appears multiple times in this
    # translation code, only the last occurrence will be used ingame.

    # If the same `old_string` is found in multiple translation files, the
    # translation from the first file to be loaded with this language
    # will be used. (This may not be the first mod to be loaded, nor the
    # file you are currently editing.)

    language = %r
    string_translation_data = {

"""
string_translation_template_end = u"""
    }
    stl = renpy.game.script.translator.strings[language]
    for (old, (new, elided, line)) in string_translation_data.viewitems():
        stl.translations.setdefault(old, new)
        stl.translation_loc.setdefault(old, (elided, line))
"""
string_translation_rpy_pyfmt_blockstart = u"init 1 python hide:"
string_translation_py_pyfmt_blockstart = u"def register_strings():\n    import renpy"

def _write_string_translations_in_file(
    file,
    language,
    strings_untranslated,
    filter,
    pyfmt,
    blockstart=string_translation_rpy_pyfmt_blockstart
):
    if pyfmt:
        file.write(
            string_translation_template_start % (
                blockstart,
                language,
            )
        )
        for s in strings_untranslated:
            text = filter(s.text)
            for location in getattr(s, 'locations', []):
                file.write(
                    u"        # {}:{}\n".format(
                        location[0],
                        location[1]
                    )
                )
            else:
                file.write(
                    u"        # {}:{}\n".format(
                        s.elided,
                        s.line
                    )
                )
            file.write(
                u"        {!r}: # old\n        ({!r}, # new\n        {!r}, {!r}),\n\n".format(
                    s.text,
                    text,
                    s.elided,
                    s.line
                )
            )
        file.write(
            string_translation_template_end
        )
        if blockstart == string_translation_py_pyfmt_blockstart and pyfmt:
            file.write(u"register_strings()")
    else:
        file.write(u"translate {} strings:\n\n".format(language))
        for s in strings_untranslated:
            text = filter(s.text)
            for loc in getattr(s, 'locations', []):
                file.write(u"    # {}:{}\n".format(loc[0], loc[1]))
            else:
                file.write(u"    # {}:{}\n".format(s.elided, s.line))
            file.write(u"    old \"{}\"\n".format(quote_unicode(s.text)))
            file.write(u"    new \"{}\"\n\n".format(quote_unicode(text)))


def write_string_translations(source, target, filter, collate, dedup, pyfmt):
    language = renpy.game.preferences.language

    if dedup:
        translated_strings = set()

    source_stl_files = translate_list_files_under(source)
    if collate:
        collated = []
    for filename in source_stl_files:
        strings = scan_strings(filename)
        strings_untranslated = get_untranslated_strings(language, strings)

        if dedup:
            # Dedup the given file
            dedup_dict = {}
            for s in strings_untranslated:
                if s.text in translated_strings:
                    continue
                if s.text not in dedup_dict:
                    dedup_dict[s.text] = s
                else:
                    old = dedup_dict[s.text]
                    locations = getattr(old, 'locations', [])
                    if not locations:
                        locations.append((old.elided, old.line))
                    locations.append((s.elided, s.line))
                    old.locations = locations
            strings_untranslated = list(dedup_dict.viewvalues())
            translated_strings.update(dedup_dict.viewkeys())

        if collate:
            collated.extend(strings_untranslated)
        elif strings_untranslated:

            fn = os.path.basename(filename)
            targetfn = os.path.join(target, fn)

            file = gtl.open_tl_file(targetfn)
            _write_string_translations_in_file(file, language, strings_untranslated, filter, pyfmt, blockstart=string_translation_rpy_pyfmt_blockstart)

    if collate:
        ext = 'py' if pyfmt else 'rpy'
        targetfn = os.path.join(target, 'strings.'+ext)
        file = gtl.open_tl_file(targetfn)
        _write_string_translations_in_file(file, language, collated, filter, pyfmt, blockstart=string_translation_py_pyfmt_blockstart)
