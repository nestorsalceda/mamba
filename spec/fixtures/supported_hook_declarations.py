with before.all:
    set_up_common_needs()

with before.each:
    set_up_concrete_stuff()

with after.each:
    pass

with after.all:
    if some_condition:
        clean_up()

    and_always_do_this()
