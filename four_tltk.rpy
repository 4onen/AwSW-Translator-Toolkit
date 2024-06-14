init python in four_tltk:
    import renpy.translation.generation as gtl
    import four_tltk as tltk

    import os

    selected_filter = gtl.empty_filter
    collate = True
    dedup = True
    pyfmt = True
    pyext = False

    def path_exists(*p):
        if len(p) > 1:
            return os.path.exists(os.path.join(*map(unicode,p)))
        else:
            return os.path.exists(*p)

    class LanguageInputValue(renpy.store.InputValue):
        def __init__(self, defaulttext):
            self.text = defaulttext
            self.default = False

        def get_text(self):
            return self.text

        def set_text(self, s):
            # allow only lowercase ascii letters
            s = s.lower()
            s = "".join([c for c in s if c in "abcdefghijklmnopqrstuvwxyz"])
            self.text = s
            renpy.restart_interaction()

        def exists(self):
            return len(self.get_text()) > 0

    language_name = LanguageInputValue("newlanguage")

    def change_language_to_given():
        renpy.change_language(language_name.get_text()+"tl")
        renpy.restart_interaction()

    def generate_base_game_language_mod():
        language_mod = language_name.get_text()+"tl"
        language_mod_path = tltk.generate_base_game_language_mod(language_mod)
        renpy.change_language(language_mod)
        target = os.path.join(language_mod_path, "resource/tl/"+language_mod)
        tltk.write_block_translations(source.get_text(), target, selected_filter)
        tltk.write_string_translations(source.get_text(), target, selected_filter, collate=collate, dedup=dedup, pyfmt=False, pyext=False)
        gtl.close_tl_files()
        renpy.quit()

    class FileInputValue(renpy.store.InputValue):
        def __init__(self, defaulttext):
            self.text = defaulttext
            self.default = False

        def get_text(self):
            return self.text

        def set_text(self, s):
            self.text = s
            renpy.restart_interaction()

        def exists(self):
            return path_exists(self.get_text())

    source = FileInputValue("game/mods/")
    target = FileInputValue("game/mods/")

    def get_true_target():
        return os.path.join(target.get_text(), "tl/"+renpy.store.preferences.language)

    def write_block_translations():
        tltk.write_block_translations(source.get_text(), get_true_target(), selected_filter)
        gtl.close_tl_files()
        renpy.quit()

    def write_string_translations():
        tltk.write_string_translations(source.get_text(), get_true_target(), selected_filter, collate=collate, dedup=dedup, pyfmt=pyfmt, pyext=pyext)
        gtl.close_tl_files()
        renpy.quit()

    def write_all_translations():
        tltk.write_block_translations(source.get_text(), get_true_target(), selected_filter)
        tltk.write_string_translations(source.get_text(), get_true_target(), selected_filter, collate=collate, dedup=dedup, pyfmt=pyfmt, pyext=pyext)
        gtl.close_tl_files()
        renpy.quit()

    class SensitiveFunction(renpy.store.Function):
        def __init__(self, sensitivity, callable, *args, **kwargs):
            super(SensitiveFunction, self).__init__(callable, *args, **kwargs)
            self.sensitivity = sensitivity

        def get_sensitive(self):
            return self.sensitivity()

    tlstats = ""

    def update_tlstats_screen():
        global tlstats

        s = tltk.calculate_tl_stats(source.get_text(), get_true_target())

        if s:
            tlstats = ("""
Src Ren'Py files found - %u
Tgt Ren'Py files found - %u
TL-able blocks found - %u
"%%s"s found - %u
TL-able blocks translated - %u
TL-able blocks missing - %u
Excess TLs - %u
""" % s) % renpy.store.preferences.language
        else:
            tlstats = "No Ren'Py files found."

    stlstats = ""

    def update_stlstats_screen():
        global stlstats
        
        s = tltk.calculate_string_stats(source.get_text())

        if s:
            stlstats = ("""
Src Ren'Py files found - %u
TL-able strings found - %u
TL-able strings translated - %u
TL-able strings missing - %u
""" % s)
        else:
            stlstats = _("No Ren'Py files found.")

init -1 python:
    style.four_tltk_button = Style(style.default)
    style.four_tltk_button_text.selected_color = "#aaf"
    style.four_tltk_button_text.insensitive_color = "#777"
    style.four_tltk_button_text.hover_color = "#ffa"
    style.four_tltk_button_text.size = 26

    style.four_tltk_warningtext = Style(style.default)
    style.four_tltk_warningtext.color = "#faa"

init:
    screen four_tltk_bg():
        modal True
        frame:
            add "black" xalign 0.5 yalign 0.5 at alpha_dissolve
            add "image/ui/ingame_menu_bg_light.png" at ingame_menu_light

        key "game_menu" action [Hide("four_tltk_bg", transition=dissolve), Hide("four_tltk_screen"), Play("audio", "se/sounds/close.ogg")]
        imagebutton idle "image/ui/close_idle.png" hover "image/ui/close_hover.png" action [Hide("four_tltk_bg", transition=dissolve), Hide("four_tltk_screen"), Play("audio", "se/sounds/close.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "smallwindowclose" xalign 0.945 yalign 0.035 at nav_button

    screen four_tltk_language_select(value):
        button action value.Enable():
            style "menu_choice_button"
            hbox:
                text "New Language:"

                input value value
                text "tl"
                if value.exists():
                    add "#3f3" size (20,20)
                else:
                    add "#f33" size (20,20)

    screen four_tltk_file_select(prefix, value, suffix=""):
        button action value.Enable():
            style "menu_choice_button"
            hbox:
                if prefix:
                    text "[prefix!t]"

                input value value
                if suffix:
                    text "[suffix]"
                if value.exists():
                    add "#3f3" size (20,20)
                else:
                    add "#f33" size (20,20)

    screen four_tltk_screen():
        vbox:
            align (0.5, 0.1)
            text _("Mod Translator's Toolkit") bold True size 40
            textbutton _("Show testscene"):
                action [Play("audio", "fx/start.ogg"), Start('four_tltk_testscene')]
                hovered Play("audio", "se/sounds/select.ogg")
                style "four_tltk_button"



        if preferences.language is None:
            text _("Select a non-default language to generate translation files.") style "four_tltk_warningtext" align (0.5, 0.5)
            hbox:
                align (0.5, 0.6)
                use four_tltk_language_select(four_tltk.language_name)
                textbutton _("Change Language"):
                    action [four_tltk.SensitiveFunction(four_tltk.language_name.exists, four_tltk.change_language_to_given), Play("audio", "se/sounds/select.ogg")]
                    hovered Play("audio", "se/sounds/select.ogg")
                    style "four_tltk_button"

        else:
            vbox:
                align (0.99, 0.1)

                textbutton _("Gen untranslated.txt."):
                    action [
                        Function(four_tltk.tltk.make_untranslated_txt,preferences.language),
                        Play("audio", "se/sounds/close.ogg"),
                        Show('nsfw_ok_prompt',dissolve,"untranslated.txt for [preferences.language] has been placed in your game directory."),
                    ]
                    hovered Play("audio", "se/sounds/select.ogg"),
                
                textbutton _("Gen overtranslated.txt."):
                    action [
                        Function(four_tltk.tltk.make_overtranslated_txt,preferences.language),
                        Play("audio", "se/sounds/close.ogg"),
                        Show('nsfw_ok_prompt',dissolve,"overtranslated.txt for [preferences.language] has been placed in your game directory."),
                    ]
                    hovered Play("audio", "se/sounds/select.ogg"),

            vbox:
                align (0.5,0.5)
                spacing 50

                vbox:
                    use four_tltk_language_select(four_tltk.language_name)
                    textbutton _("Change Language"):
                        action [four_tltk.SensitiveFunction(four_tltk.language_name.exists, four_tltk.change_language_to_given), Play("audio", "se/sounds/select.ogg")]
                        hovered Play("audio", "se/sounds/select.ogg")
                        style "four_tltk_button"
                    use four_tltk_file_select(_("Source: "), four_tltk.source)
                    use four_tltk_file_select(_("Target: "), four_tltk.target, "/tl/%s/"%preferences.language)

                    if not four_tltk.source.exists():
                        text _("No target.") style 'four_tltk_warningtext'
                    elif not four_tltk.target.exists():
                        text _("Target directory does not exist -- will be created.") style 'four_tltk_warningtext'
                    elif not four_tltk.path_exists(four_tltk.target.get_text(), 'tl', preferences.language):
                        text _("Target's translation directory does does not exist -- will be created.") style 'four_tltk_warningtext'

                hbox:
                    xminimum 1200
                    xalign 0.5
                    vbox:
                        label _("Filter:")
                        textbutton _("No filter") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.null_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                        textbutton _("Empty") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.empty_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                        textbutton _("Rot13") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.rot13_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                        textbutton _("Piglatin") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.piglatin_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"

                    vbox:
                        yminimum 300

                        textbutton _("Clear Stats") action [SetField(four_tltk,'tlstats',""), SetField(four_tltk,'stlstats',""), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"

                        if not four_tltk.tlstats:
                            textbutton _("Calculate Translation Stats") action [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.update_tlstats_screen), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                        else:
                            text "[four_tltk.tlstats!i]" size 26

                        if not four_tltk.stlstats:
                            textbutton _("Calculate String Stats") action [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.update_stlstats_screen), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                        else:
                            text "[four_tltk.stlstats!i]" size 26

                    vbox:
                        yminimum 300

                        textbutton _("Generate Basegame Language Mod"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm(_("Are you sure you want to generate a new language mod?\n`game/mods/[four_tltk.language_name.text]tl_mod/` will be created and Ren'Py will quit."),
                                    [four_tltk.SensitiveFunction(four_tltk.language_name.exists, four_tltk.generate_base_game_language_mod)]
                                )
                            ]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"

                        textbutton _("Write All Translations"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm(_("Are you sure you are ready to write translations?\n(Ren'Py will quit after finishing.)"),
                                    [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.write_all_translations)])]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"

                        textbutton _("Write Block Translations"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm(_("Are you sure you are ready to write translations?\n(Ren'Py will quit after finishing.)"),
                                    [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.write_block_translations)])]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"

                        textbutton _("Write String Translations"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm(_("Are you sure you are ready to write translations?\n(Ren'Py will quit after finishing.)"),
                                    [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.write_string_translations)])]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"

                        vbox:
                            xalign 0.5
                            # Toggle buttons for
                            # * collating string translations,
                            # * deduplicating string translations,
                            # * outputting in Python format or Ren'Py format

                            text _("String Translation Options") style "four_tltk_button_text"

                            hbox:
                                text _("Collate") style "four_tltk_button_text"
                                textbutton _("Y") action [SetField(four_tltk, 'collate', True), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                                textbutton _("N") action [SetField(four_tltk, 'collate', False), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                            hbox:
                                text _("Dedup") style "four_tltk_button_text"
                                textbutton _("Y") action [SetField(four_tltk, 'dedup', True), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                                textbutton _("N") action [SetField(four_tltk, 'dedup', False), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                            hbox:
                                text _("PyFmt") style "four_tltk_button_text"
                                textbutton _("Y") action [SetField(four_tltk, 'pyfmt', True), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                                textbutton _("N") action [SetField(four_tltk, 'pyfmt', False), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                            hbox:
                                text _("PyExt") style "four_tltk_button_text"
                                textbutton _("Y") action [SetField(four_tltk, 'pyext', True), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                                textbutton _("N") action [SetField(four_tltk, 'pyext', False), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"



label four_tltk_activate_test_language:
    $ renpy.change_language("testtl")

    jump four_tltk_activate_test_language_end
