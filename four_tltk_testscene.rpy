label four_tltk_testscene:
    s "Hello! Welcome to the translator's toolkit test scene."
    s "These SAY statements are placed in the translator's toolkit to give you an opportunity to test using the tool on a mod!"
    s "One important thing to note about translation identifiers is that, if the text they translate change, {i}they{/i} change."
    s "For text under the same label, however, the same message will have the same text."
    s "My next statement will have the same identifier as my first statement, but with an extra _1 appended to it."
    s "Hello! Welcome to the translator's toolkit test scene."
    s "When we transition to a new label, as we will with the next statement, the label part of the identifier will change, but the hash will remain the same!"
label four_tltk_testscene_second_label:
    s "Hello! Welcome to the translator's toolkit test scene."

label four_tltk_testscene_menu_tutorial:
    s "Another important thing you'll find yourself translating is {i}menu options{/i}."
    s "Menu options are considered the same as a regular string in code, as translated with the _() function."
    menu:
        "I understand that menu options are important.":
            pass
        "I understand that menu options are placed under the special {b}strings{/b} translation block.":
            pass
        "I understand I can mark a string in my code as translateable with the _() function.":
            pass
        "What?":
            pass

label four_tltk_testscene_conclusion:
    s "In any case, that's all I have. Best of luck in your modding carreer!"
    s "This is the end of the translator's toolkit test scene."
