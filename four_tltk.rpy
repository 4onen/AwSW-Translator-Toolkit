init python in four_tltk:
    import renpy.translation.generation as gtl
    import four_tltk as tltk

    selected_filter = gtl.null_filter

init:
    screen four_tltk_bg:
        modal True
        frame:
            add "black" xalign 0.5 yalign 0.5 at alpha_dissolve
            add "image/ui/ingame_menu_bg_light.png" at ingame_menu_light

        imagebutton idle "image/ui/close_idle.png" hover "image/ui/close_hover.png" action [Hide("four_tltk_bg", transition=dissolve), Hide("four_tltk_screen"), Play("audio", "se/sounds/close.ogg")] hovered Play("audio", "se/sounds/select.ogg") style "smallwindowclose" xalign 0.945 yalign 0.035 at nav_button

    screen four_tltk_screen:
        vbox:
            align (0.5,0.5)

            text _("Mod Translator's Toolkit") align (0.5, 0.1)

            # hbox:
            #     vbox:
            #         xalign 0.5
            #         text _("Filter")
            #         textbutton _("Null") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.null_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") align (0.5,0.5)
            #         textbutton _("Empty") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.empty_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") align (0.5,0.5)
            #         textbutton _("Rot13") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.rot13_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") align (0.5,0.5)
            #         textbutton _("Piglatin") action [SetField(four_tltk, 'selected_filter', four_tltk.gtl.piglatin_filter), Play("audio", "se/sounds/select.ogg")] hovered Play("audio", "se/sounds/select.ogg") align (0.5,0.5)

            textbutton "Make untranslated.txt listing all untranslated nodes in the current language.":
                action [
                    Function(four_tltk.tltk.make_untranslated_txt,preferences.language),
                    Play("audio", "se/sounds/close.ogg"),
                    Show('nsfw_ok_prompt',dissolve,"untranslated.txt has been placed in your game directory."),
                ]
                hovered Play("audio", "se/sounds/select.ogg"),
                align (0.5,0.5)


label four_tltk_activate_test_language:
    $ renpy.change_language("testtl")

    jump four_tltk_activate_test_language_end
