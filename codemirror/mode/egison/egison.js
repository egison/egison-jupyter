/**
 * CodeMirror mode for Egison 5
 * Author: Satoshi Egi
 */
CodeMirror.defineMode("egison", function () {
    var BUILTIN = "builtin", COMMENT = "comment", STRING = "string",
        ATOM = "atom", NUMBER = "number", BRACKET = "bracket",
        KEYWORD = "keyword", TYPE = "type", DEF = "def",
        VARIABLE = "variable", VARIABLE_2 = "variable-2",
        OPERATOR = "operator";

    function makeKeywords(str) {
        var obj = {}, words = str.split(" ");
        for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
        return obj;
    }

    // Type system keywords
    var typeKeywords = makeKeywords(
        "class instance inductive extends declare"
    );

    // Definition and binding keywords
    var defKeywords = makeKeywords(
        "def let in where"
    );

    // Control flow and pattern matching keywords
    var controlKeywords = makeKeywords(
        "if then else match matchDFS matchAll matchAllDFS as with do seq loop forall"
    );

    // Matcher and special form keywords
    var otherKeywords = makeKeywords(
        "matcher algebraicDataMatcher memoizedLambda cambda capply function " +
        "withSymbols pattern expression " +
        "infixr infixl infix " +
        "load loadFile execute"
    );

    // Tensor operation keywords
    var tensorKeywords = makeKeywords(
        "tensor generateTensor contract tensorMap tensorMap2 " +
        "transpose flipIndices subrefs suprefs userRefs"
    );

    // Built-in type names
    var builtinTypes = makeKeywords(
        "Integer MathExpr Float Bool Char String IO " +
        "Matcher Pattern Tensor Vector Matrix DiffForm List"
    );

    // Special values and boolean literals
    var constants = makeKeywords(
        "True False undefined something"
    );

    // Testing primitives
    var testKeywords = makeKeywords(
        "assert assertEqual"
    );

    function isIdentChar(ch) {
        return /[\w'_]/.test(ch);
    }

    function isOpChar(ch) {
        return /[+\-*\/=<>!&|^%.:~?∂∇∫∑∏√±×÷≠≤≥∞∈∉∀∃∧∨¬⊕⊗⊥⊤⊆⊇⊂⊃∪∩]/.test(ch);
    }

    function isGreek(ch) {
        return /[αβγδεζηθικλμνξοπρςστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]/.test(ch);
    }

    function tokenBase(stream, state) {
        var ch = stream.next();

        // Line comment: --
        if (ch === "-" && stream.eat("-")) {
            stream.skipToEnd();
            return COMMENT;
        }

        // Block comment: {- ... -}
        if (ch === "{" && stream.eat("-")) {
            state.commentDepth++;
            state.tokenize = tokenBlockComment;
            return tokenBlockComment(stream, state);
        }

        // String literal
        if (ch === '"') {
            state.tokenize = tokenString;
            return tokenString(stream, state);
        }

        // Character literal
        if (ch === "'") {
            if (stream.eat("\\")) {
                stream.next();
            } else {
                stream.next();
            }
            stream.eat("'");
            return STRING;
        }

        // Pattern variable: $x, $pat, or wildcard $
        if (ch === "$") {
            if (stream.match(/[a-zA-Z_][a-zA-Z0-9_']*/, true)) {
                return VARIABLE;
            }
            return VARIABLE;
        }

        // Value pattern: #x, #(expr)
        if (ch === "#") {
            if (stream.match(/[a-zA-Z_][a-zA-Z0-9_']*/, true)) {
                return ATOM;
            }
            return ATOM;
        }

        // Numbers
        if (/\d/.test(ch)) {
            stream.match(/\d*/, true);
            if (stream.eat(".")) {
                stream.match(/\d+/, true);
            }
            if (stream.eat(/[eE]/)) {
                stream.eat(/[+-]/);
                stream.match(/\d+/, true);
            }
            return NUMBER;
        }

        // Negative number
        if (ch === "-" && /\d/.test(stream.peek())) {
            stream.match(/\d*/, true);
            if (stream.eat(".")) {
                stream.match(/\d+/, true);
            }
            return NUMBER;
        }

        // Brackets
        if (/[\(\)\[\]\{\}]/.test(ch)) {
            return BRACKET;
        }

        // Tensor bracket: [| ... |]
        if (ch === "[" && stream.eat("|")) {
            return BRACKET;
        }
        if (ch === "|" && stream.eat("]")) {
            return BRACKET;
        }

        // Assignment operator :=
        if (ch === ":" && stream.eat("=")) {
            return OPERATOR;
        }

        // Cons operator ::
        if (ch === ":" && stream.eat(":")) {
            return OPERATOR;
        }

        // Arrow operators
        if (ch === "-" && stream.eat(">")) {
            return OPERATOR;
        }
        if (ch === "=" && stream.eat(">")) {
            return OPERATOR;
        }

        // Backslash (lambda)
        if (ch === "\\") {
            return KEYWORD;
        }

        // Operators
        if (isOpChar(ch)) {
            stream.eatWhile(isOpChar);
            return OPERATOR;
        }

        // Greek letters
        if (isGreek(ch)) {
            stream.eatWhile(isGreek);
            return VARIABLE_2;
        }

        // Identifiers and keywords
        if (/[a-zA-Z_]/.test(ch)) {
            stream.eatWhile(isIdentChar);
            var word = stream.current();

            if (typeKeywords.propertyIsEnumerable(word)) return KEYWORD;
            if (defKeywords.propertyIsEnumerable(word)) return KEYWORD;
            if (controlKeywords.propertyIsEnumerable(word)) return KEYWORD;
            if (otherKeywords.propertyIsEnumerable(word)) return KEYWORD;
            if (tensorKeywords.propertyIsEnumerable(word)) return BUILTIN;
            if (builtinTypes.propertyIsEnumerable(word)) return TYPE;
            if (constants.propertyIsEnumerable(word)) return ATOM;
            if (testKeywords.propertyIsEnumerable(word)) return BUILTIN;

            // User-defined types (uppercase start)
            if (/^[A-Z]/.test(word)) return TYPE;

            return null;
        }

        return null;
    }

    // Block comment tokenizer (supports nesting)
    function tokenBlockComment(stream, state) {
        var prev = null;
        while (!stream.eol()) {
            var ch = stream.next();
            if (prev === "{" && ch === "-") {
                state.commentDepth++;
            } else if (prev === "-" && ch === "}") {
                state.commentDepth--;
                if (state.commentDepth <= 0) {
                    state.commentDepth = 0;
                    state.tokenize = tokenBase;
                    return COMMENT;
                }
            }
            prev = ch;
        }
        return COMMENT;
    }

    // String tokenizer
    function tokenString(stream, state) {
        var escaped = false;
        while (!stream.eol()) {
            var ch = stream.next();
            if (ch === '"' && !escaped) {
                state.tokenize = tokenBase;
                return STRING;
            }
            escaped = !escaped && ch === "\\";
        }
        return STRING;
    }

    return {
        startState: function () {
            return {
                tokenize: tokenBase,
                commentDepth: 0
            };
        },

        token: function (stream, state) {
            if (stream.eatSpace()) return null;
            return state.tokenize(stream, state);
        },

        lineComment: "--",
        blockCommentStart: "{-",
        blockCommentEnd: "-}"
    };
});

CodeMirror.defineMIME("text/x-egison", "egison");
