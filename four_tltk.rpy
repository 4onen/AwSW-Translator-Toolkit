init python in four_tltk:
    import renpy.translation.generation as gtl
    import four_tltk as tltk

    import os

    selected_filter = gtl.empty_filter

    source = "game/mods/"
    target = "game/mods/"

    active_input = None

    def is_active_input(name):
        return active_input == name

    def check_source():
        return os.path.exists(source)

    def check_target():
        return os.path.exists(target)

init -1 python:
    style.four_tltk_button = Style(style.default)
    style.four_tltk_button_text.selected_color = "#aaf"
    style.four_tltk_button_text.insensitive_color = "#777"
    style.four_tltk_button_text.hover_color = "#ffa"
    style.four_tltk_button_text.drop_shadow = (2,2)

init:
    screen four_tltk_bg():
        modal True
        frame:
            add "black" xalign 0.5 yalign 0.5 at alpha_dissolve
            add "image/ui/ingame_menu_bg_light.png" at ingame_menu_light

        key "game_menu" action [Hide("four_tltk_bg", transition=dissolve), Hide("four_tltk_screen"), Play("audio", "se/sounds/close.ogg")]
        imagebutton idle "image/ui/close_idle.png" hover "image/ui/close_hover.png" action [Hide("four_tltk_bg", transition=dissolve), Hide("four_tltk_screen"), Play("audio", "se/sounds/close.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "smallwindowclose" xalign 0.945 yalign 0.035 at nav_button

    screen four_tltk_screen():
        text _("Mod Translator's Toolkit") align (0.5, 0.1) bold True size 40

        vbox:
            align (0.9, 0.1)

            textbutton "Gen untranslated.txt.":
                action [
                    Function(four_tltk.tltk.make_untranslated_txt,preferences.language),
                    Play("audio", "se/sounds/close.ogg"),
                    Show('nsfw_ok_prompt',dissolve,"untranslated.txt for [preferences.language] has been placed in your game directory."),
                ]
                hovered Play("audio", "se/sounds/select.ogg"),
            
            textbutton "Gen overtranslated.txt.":
                action [
                    Function(four_tltk.tltk.make_overtranslated_txt,preferences.language),
                    Play("audio", "se/sounds/close.ogg"),
                    Show('nsfw_ok_prompt',dissolve,"overtranslated.txt for [preferences.language] has been placed in your game directory."),
                ]
                hovered Play("audio", "se/sounds/select.ogg"),

        vbox:
            align (0.5,0.5)

            hbox:
                text "Source:"
                if four_tltk.is_active_input('source'):
                    input value FieldInputValue(four_tltk, 'source')
                else:
                    textbutton "[four_tltk.source]" style 'four_tltk_button':
                        hovered Play("audio", "se/sounds/select.ogg")
                        action [Play("audio", "se/sounds/select.ogg"), SetField(four_tltk, 'active_input', 'source')]
                add ConditionSwitch('four_tltk.check_source()',"#0f0","True","#f00") size (20,20)

            hbox:
                text "Target:"
                if four_tltk.is_active_input('target'):
                    input value FieldInputValue(four_tltk, 'target')
                else:
                    textbutton "[four_tltk.target]" style 'four_tltk_button':
                        hovered Play("audio", "se/sounds/select.ogg")
                        action [Play("audio", "se/sounds/select.ogg"), SetField(four_tltk, 'active_input', 'target')]
                add ConditionSwitch('four_tltk.check_target()',"#0f0","True","#f00") size (20,20)
                text "/tl/[preferences.language]/"

            hbox:
                vbox:
                    text _("Filter:")
                    textbutton _("No filter") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.null_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                    textbutton _("Empty") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.empty_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                    textbutton _("Rot13") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.rot13_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"
                    textbutton _("Piglatin") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.piglatin_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "four_tltk_button"





label four_tltk_activate_test_language:
    $ renpy.change_language("testtl")

    jump four_tltk_activate_test_language_end
