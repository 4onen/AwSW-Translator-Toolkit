init python in four_tltk:
    import renpy.translation.generation as gtl
    import four_tltk as tltk

    import os

    selected_filter = gtl.empty_filter

    def path_exists(*p):
        if len(p) > 1:
            return os.path.exists(os.path.join(*map(unicode,p)))
        else:
            return os.path.exists(*p)

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

    def write_string_translations():
        tltk.write_string_translations(source.get_text(), get_true_target(), selected_filter)
        gtl.close_tl_files()

    def write_all_translations():
        tltk.write_all_translations(source.get_text(), get_true_target(), selected_filter)
        tltk.write_string_translations(source.get_text(), get_true_target(), selected_filter)
        gtl.close_tl_files()

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
        stlstats = "String translations not yet implemented."

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

    screen four_tltk_file_select(prefix, value, suffix=""):
        button action value.Enable():
            style "menu_choice_button"
            hbox:
                if prefix:
                    text "[prefix]"

                input value value
                if value.exists():
                    add "#3f3" size (20,20)
                else:
                    add "#f33" size (20,20)
                if suffix:
                    text "[suffix]"

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
                    use four_tltk_file_select("Source: ", four_tltk.source)
                    use four_tltk_file_select("Target: ", four_tltk.target, "/tl/%s/"%preferences.language)

                    if not four_tltk.source.exists():
                        text "No target." style 'four_tltk_warningtext'
                    elif not four_tltk.target.exists():
                        text "Target directory does not exist -- will be created." style 'four_tltk_warningtext'
                    elif not four_tltk.path_exists(four_tltk.target.get_text(), 'tl', preferences.language):
                        text "Target's translation directory does does not exist -- will be created." style 'four_tltk_warningtext'

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

                        textbutton _("Write All Translations"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm("Are you sure you are ready to write translations?\n(Ren'Py will quit after finishing.)",
                                    [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.write_all_translations), Quit(confirm=False)])]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"

                        textbutton _("Write Block Translations"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm("Are you sure you are ready to write translations?\n(Ren'Py will quit after finishing.)",
                                    [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.write_block_translations), Quit(confirm=False)])]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"

                        textbutton _("Write String Translations"):
                            action [Play("audio", "se/sounds/select.ogg"),
                                Confirm("Are you sure you are ready to write translations?\n(Ren'Py will quit after finishing.)",
                                    [four_tltk.SensitiveFunction(four_tltk.source.exists, four_tltk.write_string_translations), Quit(confirm=False)])]
                            hovered Play("audio", "se/sounds/select.ogg")
                            style "four_tltk_button"




label four_tltk_activate_test_language:
    $ renpy.change_language("testtl")

    jump four_tltk_activate_test_language_end
