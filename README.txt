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
   preceeding item. "[" and "]" are used for grouping.

 start: rules ";;" python-code;
 rules: rule+;

   The entire grammar is a series of "rules" followed by two semicolons and
   then additional Python code required by the rules. "python-code" is any
   sequence of characters up to the end of the file.

   A rules has a name, an optional parameter list, and a list of alternatives
   it produces. A rules that takes parameters is called a "parameterized
   rule".

 rule: Name opt-params ":" alt ";";
 opt-params: NOTHING | "(" Name [ "," Name ]* ")";

   A list of alternatives is separated by "|". When executing the grammar,
   one of the alternatives is selected and sent to the output.

 alt: seq ["|" seq]*;

   A sequence is composed repetitions or groups:

 seq: rep | "[" alt "]";
 rep: atom ["*" | "+" | "?"]?;

   An atom is a Name with optional arguments, a String, or a call:

 atom: Name opt-args | String | call;
 opt-args: NOTHING | "(" seq [ "," seq ]* ")";

   A call is marked by "@", names the function called, and lists the
   arguments to the function:

 call: "@" dotted-name "(" args ")";
 args: arg ["," arg]* | NOTHING ;
 arg: seq | Number;
 dotted-name: Name ["." Name]*;

   Production starts with a rule called "Start" (if there is one), or the
   rule defined earliest in the file otherwise.

   Anywhere a rule is premitted, a file can be included:

 rule: "include" Name;

   The included file can define rules, and must end with ";;". No code
   portion is permitted.

                             Using parametric rules

   The simplest use of a parametric rule is to produce identical text in
   multiple places. For instance,

 Start: sentence-about(food-name);
 food-name: "tofu" | "spam";
 sentence-about(food): food " is a tasty treat.  Eat some " food " today.\n";
 ;;

   The sequence of operations is as follows: each argument is expanded in
   turn, and a temporary rule with the name of the corresponding parameter is
   created. Then, the parametric rule is expanded. Finally, the temporary
   rules are removed, and any existing with the same name is restored. As a
   result, any rule called from sentence-about will see the same expansion of
   "food" as sentence-about did. That's why the following grammar works:

 Start: sentence-about(food-name);
 food-name: "tofu" | "spam";
 sentence-about(food): positive-sentence | negative-sentence;
 positive-sentence: food " is a tasty treat.  Eat some " food " today.\n";
 negative-sentence: food " is nasty-tasting.  I can't stand " food ".\n";
 ;;

   Using a predefined @-call, @expand, you can expand the rule with the given
   name. An example:

 Start:  sentence-about(animal) ;
 animal: "dog" | "cat" ;
 sentence-about(subject): @expand(subject) " is a " subject ;
 dog: "Fido" | "Spot" ;
 cat: "Tiddles" | "Fluffy" ;
 ;;
 from novelwriting.calls import expand

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

                     novelwriting.calls: predefined @-calls

   There's a library of predefined @-calls in the module
   'novelwriting.calls'. Import from it in the code section of your grammar
   if you want to use them. These are not yet documented, and may change.
