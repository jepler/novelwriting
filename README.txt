                               About Novelwriting

   Novelwriting is a Python program for rule-based generation of text,
   similar to the Dada Engine.

   The name is chosen for the Monty Python skit, available on such recordings
   as "Monty Python The Final Rip-Off", which purports to be a live radio
   broadcast of the writing of a novel.

                  Invoking novelwriting from the command-line

 $ novelwriting spam.nw

   or

 $ novelwriting < spam.nw

                            The grammar of .nw files

   Outside of a token, whitespace is ignored.

   Comments begin with a "#" and continue until the end of the line.

   A "Name" begins with a letter or underline (_) and continues with zero or
   more letters, dashes (-), underlines or digits. For instance, these are
   all names:

     * abc
     * _123
     * A_B_C
     * a-b-c

   A "String" starts with a double quote ("), and continues to the first
   unescaped quote. Inside the string, a sequence composed of a backslash and
   another character has a special meaning:

     * \" Inserts a quote inside the string
     * \\ Inserts a backslash inside the string
     * \n Inserts a newline inside the string

   See the Python reference manual for a full explanation of the handling of
   \-escapes in a string. For instance, these are all strings:

     * "hello world"
     * "A quote: \". A backslash: \\, A newline: \n"

   A "Number" (integer) starts with an optional "-" to signify negation, a
   nonzero digit and is followed by zero or more digits (including zero), or
   simply 0. For instance, these are all numbers:

     * 0
     * 1
     * -10
     * 999

   The grammar includes other tokens. In the rules below, the required
   sequence of characters is shown inside quotation marks. "?" follows an
   optional item, "*" signals zero-or-more and "+" signals 1 or more of the
   preceeding item. "(" and ")" are used for grouping.

     start: prods ";;" python-code;
     prods: prod+;

   The entire grammar is a series of "productions" followed by two semicolons
   and then additional Python code required by the productions. "python-code"
   is any sequence of characters up to the end of the file.

   A production has a name and a list of alternatives it produces:

     prod: Name ":" alt ";";

   A list of alternatives is separated by "|". When executing the grammar,
   one of the alternatives is selected and sent to the output.

     alt: seq ("|" seq)*;

   A sequence is composed repetitions or groups:

     seq: rep | "(" alt ")";
     rep: atom ("*" | "+" | "?")?;

   An atom is a Name, a String, or a call:

     atom: Name | String | call;

   A call is marked by "@", names the function called, and lists the
   arguments to the function:

     call: "@" dotted-name "(" args ")";
     args: arg ("," arg)* | NOTHING ;
     arg: seq | Number;
     dotted-name: Name ("." Name)*;

   Production starts with a rule called "Start" (if there is one), or the
   rule defined earliest in the file otherwise.

   Anywhere a production is premitted, a file can be included:

     prod: "include" Name

                                A simple grammar

 Start: folk-saying;
 folk-saying: person " once said that " folk-saying ".\n";
 person: "My " relative | "The President" | "Cardinal Fang";
 relative: "mother" | "aunt" | "grandmother" ;
 folk-saying: "a rolling stone gathers no moss"
     | "a stitch in time saves nine"
     | "no-one expects the Spanish Inquisition";
 ;;

Two possible outputs from the grammar

 My mother once said that no-one expects the Spanish Inquisition.
 Cardinal Fang once said that a stitch in time saves nine.

         Using "@-calls" (increasing novelwriting's power with Python)

   You can execute an arbitrary Python function by writing an @-call in a
   production. The function is called with its arguments, and the return
   value is inserted into the generated output. If you write an @-call with
   dashes in the dotted-name part, the dashes are converted to underlines to
   find the function to call.

   For instance, if you wanted to output four folk sayings, you could an
   @-call:

 Start: @repeat(folk-saying, 4);

   Then, in the python-code section, you would define the "repeat" function:

 ;;
 def repeat(rule, count):
     result = []
     for i in range(count):
         result.append(str(rule))
     return "".join(result)

   Use str(rule) to generate a particular expansion of a rule.

   You can also use Names as parameters to rules, but use them to identify
   something. If you do so, you must refer to .parts[0].name. For instance,

 Start: @set(this-product, product-name) " is great.  "
     "It's better than " @alternative(product-name, @get(this-product)) ".\n"
     "Buy " @get(this-product) " today!";

 product-name: product-adj product-noun;
 product-adj: "ultra" | "mega" | "dyna";
 product-noun: "spam" | "parrot" | "python";
 ;;

 d = {}
 def set(name, val):
     name = name.parts[0].name
     d[name] = str(val)
     return d[name]

 def get(name):
     name = name.parts[0].name
     return d[name]

 def alternative(rule, excluded):
     e = str(excluded)
     while 1:
         s = str(rule)
         if s != e: return s
