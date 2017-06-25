ai.py is converted to Lua, using:
https://github.com/forcecore/pylua

However, there are a few restrictions.

  * When iterating a list, use "for x in arr:"
  * When iterating a dictionary, use "for k, v in dic.items():"
  * PyLua doesn't understand dictionary's .keys(), .values() and will not work!
  * Not a terrible thing as Lua doesn't have these either.
  * Just use "for _, v in dic.items():" if you don't need the keys and
  * Just use "for k, _ in dic.items():" if you don't need the values.

Ofcourse, you can't use Python standard libraries.
Use lua standard library instead. (See in my example script, it goes "string.lower(s)"
and such grammar is compatible with Python and nothing goes wrong.
Same for other Lua-API of OpenRA.