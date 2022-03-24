import renpy
import io

def make_untranslated_txt(language):#, min_priority, max_priority, common_only):
    """
    Prints a count of missing translations for `language`.
    """

    translator = renpy.game.script.translator

    missing_translates = set()

    # for filename in renpy.translation.generation.translate_list_files():
    #     print("Checking translations in {}".format(filename))
    #     for _, t in translator.file_translates[filename]:
    #         if (t.identifier, language) not in translator.language_translates:
    #             missing_translates.add(t.identifier)
    #         else:
    #             print(t.identifier,'is translated',t.identifier == translator.language_translates[(t.identifier, language)].identifier)
    for tlblockid, translate in translator.default_translates.items():
        if (tlblockid, language) not in translator.language_translates:
            missing_translates.add((translate.filename,translate.linenumber,tlblockid))

    # missing_strings = set()

    # stl = renpy.game.script.translator.strings[language]  # @UndefinedVariable

    # strings = renpy.translation.scanstrings.scan(common_only=False)

    # for s in strings:

    #     tlfn = renpy.translation.generation.translation_filename(s)

    #     if tlfn is None:
    #         continue

    #     if s.text in stl.translations:
    #         continue

    #     missing_strings.add(s.text)


    with io.open('untranslated.txt','w',encoding='utf-8') as f:
        f.write(u'\n'.join(sorted(map(lambda t: u':'.join(map(unicode,t)),missing_translates))))

